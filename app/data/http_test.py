import httpcore

from app.data.http_transport import create_connection_pool


pool = create_connection_pool()

try:
    request = httpcore.Request(
    method=b"GET",
    url=httpcore.URL(
        scheme=b"https",
        host=b"api.binance.com",
        port=443,
        target=b"/api/v3/time",
    ),
    headers=[
        (b"host", b"api.binance.com"),
    ],
    content=None,
    extensions={},
)

    response = pool.handle_request(request)

    print("Status:", response.status)
    print("Headers:", response.headers)
    print("Body:", response.read())

finally:
    pool.close()