from datetime import datetime, timedelta

from app.data.database import MarketDatabase
from app.data.gaps import CandleGapDetector
from app.data.models import Candle
from app.data.validation import CandleValidator


class MarketData:

    def __init__(
        self,
        database: MarketDatabase | None = None,
        symbol: str | None = None,
        interval: str | None = None,
    ):
        self.candles: list[Candle] = []

        self.database = database
        self.symbol = symbol
        self.interval = interval

    def add_candle(self, candle: Candle):
        # Validate the candle's OHLCV values.
        CandleValidator.validate(candle)

        # Make sure candles arrive in chronological order.
        if self.candles:
            last_timestamp = self.candles[-1].timestamp

            if candle.timestamp <= last_timestamp:
                raise ValueError(
                    "Candle timestamp must be newer than the latest candle"
                )

        # Persist first.
        if self.database is not None:

            if self.symbol is None or self.interval is None:
                raise ValueError(
                    "Symbol and interval are required when using a database"
                )

            self.database.save_candle(
                symbol=self.symbol,
                interval=self.interval,
                candle=candle,
            )

        # Only update memory after persistence succeeds.
        self.candles.append(candle)

    def add_candles(self, candles: list[Candle]):
        for candle in candles:
            self.add_candle(candle)

    def load_from_database(self):
        if self.database is None:
            raise ValueError("Database is not configured")

        if self.symbol is None or self.interval is None:
            raise ValueError(
                "Symbol and interval are required when using a database"
            )

        self.candles = self.database.load_candles(
            symbol=self.symbol,
            interval=self.interval,
        )

    def get_candles(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[Candle]:

        result = self.candles

        if start is not None:
            result = [
                candle
                for candle in result
                if candle.timestamp >= start
            ]

        if end is not None:
            result = [
                candle
                for candle in result
                if candle.timestamp <= end
            ]

        return result

    def latest(self, count: int = 1) -> list[Candle]:

        if count < 1:
            raise ValueError("Count must be greater than 0")

        return self.candles[-count:]

    def find_gaps(
        self,
        interval: timedelta,
    ) -> list[tuple[Candle, Candle]]:

        return CandleGapDetector.find_gaps(
            self.candles,
            interval,
        )

    def load_latest(self, count: int = 1) -> list[Candle]:

        if self.database is None:
            raise ValueError("Database is not configured")

        if self.symbol is None or self.interval is None:
            raise ValueError(
             "Symbol and interval are required when using a database"
        )

    return self.database.load_latest_candles(
        symbol=self.symbol,
        interval=self.interval,
        limit=count,
    )    