from app.data.models import Candle
from app.data.validation import CandleValidator
from app.data.database import MarketDatabase


class HistoricalDataIngestion:

    @staticmethod
    def validate_candles(candles: list[Candle]) -> None:
        for candle in candles:
            CandleValidator.validate(candle)

        for previous, current in zip(candles, candles[1:]):
            if current.timestamp <= previous.timestamp:
                raise ValueError("Candles must be in chronological order")

    @staticmethod
    def ingest(
        database: MarketDatabase,
        symbol: str,
        interval: str,
        candles: list[Candle],
    ) -> int:

        HistoricalDataIngestion.validate_candles(candles)

        return database.save_candles(
            symbol=symbol,
            interval=interval,
            candles=candles,
        )