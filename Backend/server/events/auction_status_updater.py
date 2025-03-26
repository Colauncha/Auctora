import asyncio
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from ..models.auction import Auctions
from ..config.database import get_db
from ..enums.auction_enums import AuctionStatus
from ..services.auction_service import AuctionServices


# Scheduler instance
scheduler = AsyncIOScheduler()

async def update_status():
    session: Session = next(get_db())
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
                print(f"♻ Updating status for event {event.id} to {AuctionStatus.ACTIVE}")
                event.status = AuctionStatus.ACTIVE
                print('✅ Event status updated')
                update = True
            elif event.status == AuctionStatus.ACTIVE and current_time >= event.end_date:
                print(f"♻ Updating status for event {event.id} to {AuctionStatus.COMPLETED}")
                event.status = AuctionStatus.COMPLETED
                await AuctionServices(session).close(event.id)
                print('✅ Event status updated')
                update = True

        # Commit changes
        if update:
            session.commit()
            print("🔄 Status updated successfully")
        else:
            print("🔄 No events to update")
    except Exception as e:
        print(f"Error updating status: {e}")
    finally:
        session.close()

# Keep the script running
async def main():
    scheduler.add_job(update_status, 'interval', seconds=15)
    scheduler.start()
    try:
        print("⏳ Scheduler started. Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n❌ Scheduler stopped")
