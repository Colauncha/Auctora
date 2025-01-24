from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..models.auction import Auctions
from ..config.database import get_db
from ..enums.auction_enums import AuctionStatus


# Scheduler instance
scheduler = BackgroundScheduler()


def update_status():
    session: Session = next(get_db())
    try:
        # Query events where the status needs updating
        events = session.query(Auctions).filter(
            (Auctions.status == AuctionStatus.PENDING and Auctions.start_date <= datetime.now()) |
            (Auctions.status == AuctionStatus.ACTIVE and Auctions.end_date <= datetime.now())
        ).with_for_update().all()

        for event in events:
            current_time = datetime.now(timezone.utc)
            update = False
            if event.status == AuctionStatus.PENDING and current_time >= event.start_date:
                print(f"♻ Updating status for event {event.id} to {AuctionStatus.ACTIVE}")
                event.status = AuctionStatus.ACTIVE
                print('✅ Event status updated')
                update = True
            elif event.status == AuctionStatus.ACTIVE and current_time >= event.end_date:
                print(f"♻ Updating status for event {event.id} to {AuctionStatus.COMPLETED}")
                event.status = AuctionStatus.COMPLETED
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

# Schedule the job to run every minute (or any interval you need)
scheduler.add_job(update_status, 'interval', minutes=1)

# Start the scheduler
scheduler.start()

# Keep the script running
try:
    print("⏳ Scheduler started. Press Ctrl+C to exit.")
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
