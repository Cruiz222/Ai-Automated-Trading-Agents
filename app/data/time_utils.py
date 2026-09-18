from datetime import datetime, timezone


def normalize_to_utc(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is None:
        raise ValueError("Timestamp must be timezone-aware")

    return timestamp.astimezone(timezone.utc)
