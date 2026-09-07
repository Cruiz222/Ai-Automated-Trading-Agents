import requests

from app.data.dns import DoHResolver


resolver = DoHResolver()

hostname = "api.binance.com"
ip = resolver.resolve(hostname)[0]

print("Resolved:", hostname, "->", ip)

response = requests.get(
    f"https://{ip}/api/v3/time",
    headers={
        "Host": hostname,
    },
    timeout=10,
    verify=True,
)

print(response.status_code)
print(response.text)