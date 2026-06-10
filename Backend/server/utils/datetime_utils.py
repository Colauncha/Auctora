from datetime import datetime, timezone
from zoneinfo import ZoneInfo

WAT = ZoneInfo("Africa/Lagos")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_wat() -> datetime:
    """Returns current time in West African Time — for display/user-facing contexts only."""
    return datetime.now(WAT)
