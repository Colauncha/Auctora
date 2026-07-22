import asyncio
import logging
from datetime import datetime, timezone
from server.utils.datetime_utils import now_utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from ..models.auction import Auctions
from ..models.payment import Payments
from ..config.database import app_configs, _async_url
from ..enums.auction_enums import AuctionStatus
from ..enums.payment_enums import PaymentStatus
from ..services import (
    AuctionServices,
    DBAdaptor,
    UserNotificationServices,
    ChatServices,
    RewardHistoryService,
)


# Separate process: its own async engine. NullPool avoids holding idle
# connections between scheduler ticks.
engine = create_async_engine(
    _async_url(app_configs.DB.DATABASE_URL),
    poolclass=NullPool,
    pool_pre_ping=True,
)
SessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)

# Configure logging
LOG_FILE_PATH = '/var/log/biddius-logs/auction_updater.log'\
if app_configs.ENV == 'production' else 'auction_updater.log'

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Scheduler instance
scheduler = AsyncIOScheduler()

async def update_status(auctionServices: AuctionServices):
    session: AsyncSession = SessionLocal()
    try:
        update = False
        # Query events where the status needs updating
        _now = now_utc()
        events = (await session.execute(
            select(Auctions).filter(
                (Auctions.status == AuctionStatus.PENDING) & (Auctions.start_date <= _now) |
                (Auctions.status == AuctionStatus.ACTIVE) & (Auctions.end_date <= _now)
            ).with_for_update()
        )).scalars().all()

        for event in events:
            current_time = datetime.now(timezone.utc)
            if event.status == AuctionStatus.PENDING and current_time >= event.start_date:
                logger.info(f"♻ Updating status for event {event.id} to {AuctionStatus.ACTIVE}")
                event.status = AuctionStatus.ACTIVE
                logger.info('✅ Event status updated')
                update = True
            elif event.status == AuctionStatus.ACTIVE and current_time >= event.end_date:
                logger.info(f"♻ Updating status for event {event.id} to {AuctionStatus.COMPLETED}")
                await auctionServices.close(event.id, db=session)
                logger.info('✅ Event status updated')
                update = True

        # Commit changes
        if update:
            await session.commit()
            logger.info("🔄 Status updated successfully")

    except Exception as e:
        logger.error(f"Error updating status: {e}")
    finally:
        await session.close()


async def process_intra_payment(auctionServices: AuctionServices):
    session: AsyncSession = SessionLocal()
    update = False

    try:
        current_time = now_utc()

        # Auto-finalize PENDING and INSPECTING payments that have passed their due date
        finalize_events = (await session.execute(
            select(Payments).filter(
                Payments.status.in_([PaymentStatus.PENDING, PaymentStatus.INSPECTING]),
                Payments.due_data <= current_time
            ).with_for_update()
        )).scalars().all()

        for event in finalize_events:
            logger.info(
                f"♻ Auto-finalizing payment {event.id} from {event.from_id} to {event.to_id}"
            )
            await auctionServices.finalize_payment(
                event.auction_id, event.from_id, db=session
            )
            logger.info('✅ Payment finalized')
            update = True

        # Auto-confirm REFUNDING payments the seller has not responded to within the deadline
        refund_events = (await session.execute(
            select(Payments).filter(
                Payments.status == PaymentStatus.REFUNDING,
                Payments.due_data <= current_time
            ).with_for_update()
        )).scalars().all()

        for event in refund_events:
            logger.info(
                f"♻ Auto-confirming overdue refund {event.id} for buyer {event.from_id}"
            )
            await auctionServices.auto_complete_refund(event.auction_id, db=session)
            logger.info('✅ Refund auto-confirmed')
            update = True

        if update:
            await session.commit()
            logger.info("🔄 Payment status updated successfully")
    except Exception as e:
        logger.error(f"Error processing intra payment: {e}")
    finally:
        await session.close()

# Keep the script running
async def main():
    # Services and Repos
    factory = DBAdaptor().factory()

    user_repo = factory.user_repo(factory.wallet_repo())
    notif_service = UserNotificationServices(factory.notif_repo())
    chat_service = ChatServices(factory.chat_repo())
    reward_service = RewardHistoryService(
        factory.rewardhistory_repo(), user_repo, notif_service
    )

    auction_service = AuctionServices(
        auction_p_repo=factory.auction_p_repo(),
        auction_repo=factory.auction_repo(factory.auction_p_repo()),
        user_repo=user_repo,
        payment_repo=factory.payment_repo(),
        notif_service=notif_service,
        chat_service=chat_service,
        reward_service=reward_service,
    )

    scheduler.add_job(
        update_status,
        'interval',
        seconds=15,
        args=[auction_service]
    )
    scheduler.add_job(
        process_intra_payment,
        'interval',
        seconds=30,
        args=[auction_service]
    )
    scheduler.start()

    try:
        logger.info("⏳ Scheduler started. Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("❌ Scheduler stopped")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n❌ Scheduler stopped")
