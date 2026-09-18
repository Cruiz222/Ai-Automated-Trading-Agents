from datetime import datetime, timezone, timedelta

from app.data.gaps import CandleGapDetector
from app.data.models import Candle


candles = [
    Candle(
        timestamp=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
        open=100,
        high=105,
        low=99,
        close=103,
        volume=10,
    ),
    Candle(
        timestamp=datetime(2026, 9, 1, 12, 1, tzinfo=timezone.utc),
        open=103,
        high=107,
        low=102,
        close=106,
        volume=12,
    ),
    Candle(
        timestamp=datetime(2026, 9, 1, 12, 3, tzinfo=timezone.utc),
        open=109,
        high=112,
        low=108,
        close=111,
        volume=18,
    ),
]


gaps = CandleGapDetector.find_gaps(
    candles,
    timedelta(minutes=1),
)


print("Gaps found:", len(gaps))

for previous, current in gaps:
    print(
        "Gap between:",
        previous.timestamp,
        "and",
        current.timestamp,
    )