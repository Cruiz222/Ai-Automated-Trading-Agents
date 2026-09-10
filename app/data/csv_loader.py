import csv
from datetime import datetime

from app.data.models import Candle


class CSVLoader:

    @staticmethod
    def load(filepath: str) -> list[Candle]:

        candles = []

        with open(filepath, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                candle = Candle(
                    timestamp=datetime.fromisoformat(
                        row["timestamp"]
                    ),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                )

                candles.append(candle)

        return candles