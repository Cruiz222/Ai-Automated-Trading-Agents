import sqlite3
from datetime import datetime

from app.data.models import Candle


class DuplicateCandleError(Exception):
    pass


class MarketDatabase:

    def __init__(self, database_path: str = "data/market.db"):
        self.connection = sqlite3.connect(database_path)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS candles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                interval TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume REAL NOT NULL,

                UNIQUE(symbol, interval, timestamp)
            )
        """)

        self.connection.commit()

    def save_candle(
        self,
        symbol: str,
        interval: str,
        candle: Candle,
    ) -> None:

        try:

            self.connection.execute(
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
                    symbol,
                    interval,
                    candle.timestamp.isoformat(),
                    candle.open,
                    candle.high,
                    candle.low,
                    candle.close,
                    candle.volume,
                ),
            )

            self.connection.commit()

        except sqlite3.IntegrityError as error:

            raise DuplicateCandleError(
                "Candle already exists for "
                f"{symbol} {interval} "
                f"at {candle.timestamp}"
            ) from error

    def load_candles(
        self,
        symbol: str,
        interval: str,
    ) -> list[Candle]:

        cursor = self.connection.execute(
            """
            SELECT
                timestamp,
                open,
                high,
                low,
                close,
                volume
            FROM candles
            WHERE symbol = ?
              AND interval = ?
            ORDER BY timestamp ASC
            """,
            (
                symbol,
                interval,
            ),
        )

        rows = cursor.fetchall()

        candles = []

        for row in rows:
            candles.append(
                Candle(
                    timestamp=datetime.fromisoformat(row[0]),
                    open=row[1],
                    high=row[2],
                    low=row[3],
                    close=row[4],
                    volume=row[5],
                )
            )

        return candles

    def close(self) -> None:
        self.connection.close()