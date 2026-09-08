from datetime import timedelta

from app.data.models import Candle


class CandleGapDetector:

    @staticmethod
    def find_gaps(
        candles: list[Candle],
        interval: timedelta,
    ) -> list[tuple[Candle, Candle]]:

        gaps = []

        for previous, current in zip(candles, candles[1:]):

            expected_timestamp = previous.timestamp + interval

            if current.timestamp > expected_timestamp:
                gaps.append((previous, current))

        return gaps