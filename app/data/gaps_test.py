from datetime import datetime, timedelta, timezone

from app.data.gaps import CandleGapDetector
from app.data.models import Candle


candles = [
    Candle(
        timestamp=datetime(
            2026, 9, 1, 12, 0,
            tzinfo=timezone.utc,
        ),
        open=100,
        high=105,
        low=99,
        close=103,
        volume=10,
    ),

    Candle(
        timestamp=datetime(
            2026, 9, 1, 12, 1,
            tzinfo=timezone.utc,
        ),
        open=103,
        high=107,
        low=102,
        close=106,
        volume=12,
    ),

    Candle(
        timestamp=datetime(
            2026, 9, 1, 12, 2,
            tzinfo=timezone.utc,
        ),
        open=106,
        high=108,
        low=105,
        close=107,
        volume=15,
    ),

    # 12:03 is intentionally missing

    Candle(
        timestamp=datetime(
            2026, 9, 1, 12, 4,
            tzinfo=timezone.utc,
        ),
        open=107,
        high=109,
        low=106,
        close=108,
        volume=11,
    ),
]


gaps = CandleGapDetector.find_gaps(
    candles,
    timedelta(minutes=1),
)


print("Number of gaps:", len(gaps))

for previous, current in gaps:
    print(
        "Gap between:",
        previous.timestamp,
        "and",
        current.timestamp,
    )