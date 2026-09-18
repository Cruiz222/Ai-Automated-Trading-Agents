from app.data.models import Candle
from app.data.validation import CandleValidator
from app.data.database import MarketDatabase
from datetime import timedelta
from app.data.gaps import CandleGapDetector
from app.data.quality import DataQualityReport

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

    @staticmethod
    def find_gaps(
        candles: list[Candle],
        interval: timedelta,
    ) -> list[tuple[Candle, Candle]]:
        return CandleGapDetector.find_gaps(
            candles,
            interval,
        )  

    @staticmethod
    def quality_report(
        candles: list[Candle],
        interval: timedelta,
    ) -> DataQualityReport:

        HistoricalDataIngestion.validate_candles(candles)

        gaps = HistoricalDataIngestion.find_gaps(
            candles,
            interval,
        )

        return DataQualityReport(
            candle_count=len(candles),
            gaps=gaps,
        )      