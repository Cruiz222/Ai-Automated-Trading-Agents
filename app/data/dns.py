import requests


class DoHResolver:

    URL = "https://cloudflare-dns.com/dns-query"

    def resolve(self, hostname: str) -> list[str]:

        response = requests.get(
            self.URL,
            params={
                "name": hostname,
                "type": "A",
            },
            headers={
                "accept": "application/dns-json",
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        addresses = []

        for answer in data.get("Answer", []):
            if answer.get("type") == 1:
                addresses.append(answer["data"])

        return addresses