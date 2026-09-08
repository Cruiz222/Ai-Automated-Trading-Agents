from datetime import datetime, timedelta, timezone

from app.data.market_data import MarketData
from app.data.models import Candle


# ============================================================
# Basic MarketData tests
# ============================================================

market = MarketData()


# Add first candle
market.add_candle(
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
    )
)


# Add second candle
market.add_candle(
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
    )
)


print("All candles:")
print(market.get_candles())


print("\nLatest candle:")
print(market.latest())


print("\nLatest 2 candles:")
print(market.latest(2))


# ============================================================
# Duplicate timestamp test
# ============================================================

try:
    market.add_candle(
        Candle(
            timestamp=datetime(
                2026, 9, 1, 12, 1,
                tzinfo=timezone.utc,
            ),
            open=106,
            high=110,
            low=105,
            close=109,
            volume=15,
        )
    )

except ValueError as error:
    print("\nDuplicate timestamp rejected:")
    print(error)


# ============================================================
# Out-of-order timestamp test
# ============================================================

try:
    market.add_candle(
        Candle(
            timestamp=datetime(
                2026, 9, 1, 11, 59,
                tzinfo=timezone.utc,
            ),
            open=99,
            high=101,
            low=98,
            close=100,
            volume=8,
        )
    )

except ValueError as error:
    print("\nOut-of-order timestamp rejected:")
    print(error)


# ============================================================
# Gap detection test
# ============================================================

gap_market = MarketData()


# 12:00
gap_market.add_candle(
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
    )
)


# 12:01
gap_market.add_candle(
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
    )
)


# 12:02 is intentionally missing.


# 12:03
gap_market.add_candle(
    Candle(
        timestamp=datetime(
            2026, 9, 1, 12, 3,
            tzinfo=timezone.utc,
        ),
        open=106,
        high=108,
        low=105,
        close=107,
        volume=15,
    )
)


gaps = gap_market.find_gaps(
    timedelta(minutes=1)
)


print("\nGaps detected:", len(gaps))


for previous, current in gaps:
    print(
        "Gap:",
        previous.timestamp,
        "->",
        current.timestamp,
    )