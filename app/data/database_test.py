from datetime import datetime, timezone

from app.data.database import (
    DuplicateCandleError,
    MarketDatabase,
)
from app.data.market_data import MarketData
from app.data.models import Candle


# ============================================================
# Create in-memory database
# ============================================================

database = MarketDatabase(":memory:")


# ============================================================
# Create MarketData
# ============================================================

market = MarketData(
    database=database,
    symbol="BTCUSDT",
    interval="1m",
)


# ============================================================
# Create candles
# ============================================================

candle1 = Candle(
    timestamp=datetime(
        2026,
        9,
        1,
        12,
        0,
        tzinfo=timezone.utc,
    ),
    open=100,
    high=105,
    low=99,
    close=103,
    volume=10,
)


candle2 = Candle(
    timestamp=datetime(
        2026,
        9,
        1,
        12,
        1,
        tzinfo=timezone.utc,
    ),
    open=103,
    high=107,
    low=102,
    close=106,
    volume=12,
)


# ============================================================
# Save candles through MarketData
# ============================================================

market.add_candle(candle1)
market.add_candle(candle2)


print("Candles saved successfully.")


# ============================================================
# Check MarketData memory
# ============================================================

print("\nCandles currently in memory:")

for candle in market.get_candles():
    print(candle)


# ============================================================
# Clear memory
# ============================================================

market.candles.clear()


print("\nMemory cleared:")
print(market.get_candles())


# ============================================================
# Reload from database
# ============================================================

market.load_from_database()


print("\nCandles loaded from database:")

for candle in market.get_candles():
    print(candle)


# ============================================================
# Duplicate test
# ============================================================

print("\nTesting database duplicate protection:")

try:

    database.save_candle(
        symbol="BTCUSDT",
        interval="1m",
        candle=candle1,
    )

except DuplicateCandleError as error:

    print("Duplicate rejected:")
    print(error)

# ============================================================
# Close database
# ============================================================

database.close()