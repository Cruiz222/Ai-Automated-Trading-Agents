from app.data.csv_loader import CSVLoader


candles = CSVLoader.load(
    "data/test_candles.csv"
)

print("Loaded candles:", len(candles))

for candle in candles:
    print(candle)

print("\nTimestamp type:")
print(type(candles[0].timestamp))