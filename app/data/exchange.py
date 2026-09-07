import requests

from app.data.models import Candle


class ExchangeClient:

    BASE_URL = "https://api.binance.com"

    def get_candles(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 100,
    ) -> list[Candle]:

        url = f"{self.BASE_URL}/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        candles = []

        for item in data:
            candle = Candle(
                timestamp=item[0],
                open=float(item[1]),
                high=float(item[2]),
                low=float(item[3]),
                close=float(item[4]),
                volume=float(item[5]),
            )

            candles.append(candle)

        return candles