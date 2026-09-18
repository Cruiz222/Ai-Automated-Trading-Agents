from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self):
        if self.timestamp.tzinfo is None:
            raise ValueError("Candle timestamp must be timezone-aware")

        self.timestamp = self.timestamp.astimezone(timezone.utc)