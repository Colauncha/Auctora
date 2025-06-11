import asyncio
import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from ..models.auction import Auctions
from ..models.payment import Payments
from ..config.database import get_db, app_configs
from ..enums.auction_enums import AuctionStatus
from ..enums.payment_enums import PaymentStatus
from ..services.auction_service import AuctionServices

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

async def update_status():
    session: Session = next(get_db())
    count = 1
    try:
        update = False
        # Query events where the status needs updating
        events = session.query(Auctions).filter(
            (Auctions.status == AuctionStatus.PENDING and Auctions.start_date <= datetime.now()) |
            (Auctions.status == AuctionStatus.ACTIVE and Auctions.end_date <= datetime.now())
        ).with_for_update().all()

        for event in events:
            current_time = datetime.now(timezone.utc)
            if event.status == AuctionStatus.PENDING and current_time >= event.start_date:
                logger.info(f"♻ Updating status for event {event.id} to {AuctionStatus.ACTIVE}")
                event.status = AuctionStatus.ACTIVE
                logger.info('✅ Event status updated')
                update = True
            elif event.status == AuctionStatus.ACTIVE and current_time >= event.end_date:
                logger.info(f"♻ Updating status for event {event.id} to {AuctionStatus.COMPLETED}")
                event.status = AuctionStatus.COMPLETED
                await AuctionServices(session).close(event.id)
                logger.info('✅ Event status updated')
                update = True

        # Commit changes
        if update:
            session.commit()
            logger.info("🔄 Status updated successfully")
        else:
            pass
            # logger.info("🔄 No events to update")

    except Exception as e:
        logger.error(f"Error updating status: {e}")
    finally:
        session.close()


async def process_intra_payment():
    session: Session = next(get_db())
    update = False

    try:
        events = session.query(Payments).filter(
            ((Payments.status == 'INSPECTING' or Payments.status == 'PENDING') and Payments.due_data <= datetime.now()) 
        ).with_for_update().all()
        print(datetime.now().astimezone())
        for event in events:
            current_time = datetime.now().astimezone()
            print(current_time >= event.due_data)
            if (event.status != PaymentStatus.PENDING or event.status != PaymentStatus.INSPECTING) and current_time >= event.due_data:
                print(f'running event {event.id}...')
                logger.info(
                    f"♻ Updating status for payment {event.id} from {event.from_id} to {event.to_id}"
                )
                await AuctionServices(session).finalize_payment(event.auction_id, event.from_id)
                # event.status = 'COMPLETED'
                print('Done')
                logger.info('✅ Payment status updated')
                update = True
        
        if update:
            session.commit()
            logger.info("🔄 Payment status updated successfully")
        else:
            pass
    except Exception as e:
        print(e.with_traceback())
        logger.error(f"Error processing intra payment: {e}")
    finally:
        session.close()

# Keep the script running
async def main():
    scheduler.add_job(update_status, 'interval', seconds=15)
    scheduler.add_job(process_intra_payment, 'interval', seconds=30)
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
