import sqlite3
from datetime import datetime, timezone

from app.data.database import MarketDatabase
from app.data.models import Candle


database = MarketDatabase(":memory:")

candle1 = Candle(
    timestamp=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
    open=100,
    high=105,
    low=99,
    close=103,
    volume=10,
)

candle2 = Candle(
    timestamp=datetime(2026, 9, 1, 12, 1, tzinfo=timezone.utc),
    open=103,
    high=107,
    low=102,
    close=106,
    volume=12,
)


database.save_candle(
    symbol="BTCUSDT",
    interval="1m",
    candle=candle1,
)


print("Before batch:")
print(
    "Candles:",
    len(database.load_candles("BTCUSDT", "1m")),
)


try:
    database.connection.execute(
        """
        INSERT INTO candles (
            symbol,
            interval,
            timestamp,
            open,
            high,
            low,
            close,
            volume
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "BTCUSDT",
            "1m",
            candle1.timestamp.isoformat(),
            candle1.open,
            candle1.high,
            candle1.low,
            candle1.close,
            candle1.volume,
        ),
    )

    database.connection.commit()

except sqlite3.IntegrityError:
    database.connection.rollback()
    print("\nDuplicate detected.")
    print("Transaction rolled back.")


print("\nAfter failure:")
print(
    "Candles:",
    len(database.load_candles("BTCUSDT", "1m")),
)


database.close()