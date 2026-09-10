from app.data.database import MarketDatabase
from app.data.csv_loader import CSVLoader
from app.data.ingestion import HistoricalDataIngestion


database = MarketDatabase(":memory:")

candles = CSVLoader.load("data/test_candles.csv")

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

print("\nCandles in database:")
print("Total:", len(loaded))

database.close()