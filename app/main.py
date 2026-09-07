from app.data.exchange import ExchangeClient


client = ExchangeClient()

candles = client.get_candles(
    symbol="BTCUSDT",
    interval="1m",
    limit=5,
)

for candle in candles:
    print(candle)