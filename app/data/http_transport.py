import httpcore

from app.data.dns import DoHResolver


class DoHBackend(httpcore.NetworkBackend):

    def __init__(self):
        self.resolver = DoHResolver()
        self.backend = httpcore.SyncBackend()

    def connect_tcp(
        self,
        host: str,
        port: int,
        timeout: float | None = None,
        local_address: str | None = None,
        socket_options=None,
    ) -> httpcore.NetworkStream:

        addresses = self.resolver.resolve(host)

        if not addresses:
            raise OSError(f"Could not resolve {host}")

        last_error = None

        for address in addresses:
            try:
                return self.backend.connect_tcp(
                    address,
                    port,
                    timeout,
                    local_address,
                    socket_options,
                )
            except OSError as error:
                last_error = error

        raise OSError(
            f"Could not connect to {host}"
        ) from last_error

    def connect_unix_socket(
        self,
        path: str,
        timeout: float | None = None,
        socket_options=None,
    ) -> httpcore.NetworkStream:

        return self.backend.connect_unix_socket(
            path,
            timeout,
            socket_options,
        )

    def sleep(self, seconds: float) -> None:
        self.backend.sleep(seconds)


def create_connection_pool() -> httpcore.ConnectionPool:
    return httpcore.ConnectionPool(
        network_backend=DoHBackend(),
        max_connections=10,
        max_keepalive_connections=5,
        keepalive_expiry=5.0,
    )