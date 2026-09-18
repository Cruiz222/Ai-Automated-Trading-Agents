from app.data.database import MarketDatabase
from app.data.csv_loader import CSVLoader
from app.data.ingestion import HistoricalDataIngestion
from datetime import timedelta


database = MarketDatabase(":memory:")

candles = CSVLoader.load("data/test_candles.csv")
gapped_candles = [
    candles[0],
    candles[1],
    candles[3],
]

inserted = HistoricalDataIngestion.ingest(
    database=database,
    symbol="BTCUSDT",
    interval="1m",
    candles=candles,
)

print("First ingestion:")
print("New candles inserted:", inserted)

inserted_again = HistoricalDataIngestion.ingest(
    database=database,
    symbol="BTCUSDT",
    interval="1m",
    candles=candles,
)

print("\nSecond ingestion:")
print("New candles inserted:", inserted_again)

loaded = database.load_candles(
    symbol="BTCUSDT",
    interval="1m",
)

print("\nTesting gap detection:")

gaps = HistoricalDataIngestion.find_gaps(
    gapped_candles,
    timedelta(minutes=1),
)

print("Gaps found:", len(gaps))

for previous, current in gaps:
    print(
        "Gap between:",
        previous.timestamp,
        "and",
        current.timestamp,
    )

database.close()