from datetime import datetime, timezone

from app.data.database import MarketDatabase
from app.data.models import Candle


database = MarketDatabase(":memory:")


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
        high=110,
        low=105,
        close=109,
        volume=15,
    ),
    Candle(
        timestamp=datetime(
            2026, 9, 1, 12, 3,
            tzinfo=timezone.utc,
        ),
        open=109,
        high=112,
        low=108,
        close=111,
        volume=18,
    ),
]


for candle in candles:
    database.save_candle(
        symbol="BTCUSDT",
        interval="1m",
        candle=candle,
    )


print("=== ALL CANDLES ===")

result = database.load_candles(
    symbol="BTCUSDT",
    interval="1m",
)

for candle in result:
    print(candle)


print("\n=== TIME RANGE ===")

result = database.load_candles(
    symbol="BTCUSDT",
    interval="1m",
    start=datetime(
        2026, 9, 1, 12, 1,
        tzinfo=timezone.utc,
    ),
    end=datetime(
        2026, 9, 1, 12, 2,
        tzinfo=timezone.utc,
    ),
)

for candle in result:
    print(candle)


print("\n=== LIMIT ===")

result = database.load_candles(
    symbol="BTCUSDT",
    interval="1m",
    limit=2,
)

for candle in result:
    print(candle)


print("\n=== LATEST 2 CANDLES ===")

result = database.load_latest_candles(
    symbol="BTCUSDT",
    interval="1m",
    limit=2,
)

for candle in result:
    print(candle)

database.close()