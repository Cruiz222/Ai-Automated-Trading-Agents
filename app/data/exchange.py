from datetime import datetime, timezone

import httpcore

from app.data.http_transport import create_connection_pool
from app.data.models import Candle


class ExchangeClient:

    def __init__(self):
        self.pool = create_connection_pool()

    def get_candles(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 100,
    ) -> list[Candle]:

        request = httpcore.Request(
            method=b"GET",
            url=httpcore.URL(
    scheme=b"https",
    host=b"api.binance.com",
    port=443,
    target=(
        f"/api/v3/klines"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&limit={limit}"
    ).encode(),
),
            headers=[
                (b"host", b"api.binance.com"),
            ],
            content=None,
            extensions={},
        )

        response = self.pool.handle_request(request)

        try:
            if response.status != 200:
                raise RuntimeError(
                    f"Binance API returned status {response.status}"
                )

            data = response.read()

        finally:
            response.close()

        import json

        data = json.loads(data)

        candles = []

        for item in data:
            candles.append(
                Candle(
                    timestamp=datetime.fromtimestamp(
                        item[0] / 1000,
                        tz=timezone.utc,
                    ),
                    open=float(item[1]),
                    high=float(item[2]),
                    low=float(item[3]),
                    close=float(item[4]),
                    volume=float(item[5]),
                )
            )

        return candles

    def close(self):
        self.pool.close()