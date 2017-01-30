import asyncio


class ServerProtocol(asyncio.Protocol):
    CLIENT_TIMEOUT_IN_SEC = 10.0
    HEARTBEAT_PERIOD_IN_SEC = 2.0

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(self.peername))
        self.transport = transport

        self._setup_client_timeout()
        self._heartbeat()

    def data_received(self, data):
        print("Data received from {}".format(self.peername))

        self.client_timeout_handle.cancel()
        self._setup_client_timeout()

        try:
            message = data.decode()
            print('\t{!r}'.format(message))
        except UnicodeDecodeError:
            print("Unable to decode string: {!r}".format(data))

    def connection_lost(self, exception):
        if exception:
            print(
                "Server shutdown due to exception: {}".format(exception))
        print("Shut down connection with {}".format(self.peername))
        self.heartbeat_handle.cancel()
        self.client_timeout_handle.cancel()
        self.transport.close()

    def _setup_client_timeout(self):
        self.client_timeout_handle = asyncio.get_event_loop().call_later(
            self.CLIENT_TIMEOUT_IN_SEC, self._client_timed_out)

    def _client_timed_out(self):
        print("Connection timeout, closing {}".format(self.peername))
        self.transport.close()

    def _heartbeat(self):
        self.transport.write(b"\"heartbeat\"")
        self.heartbeat_handle = asyncio.get_event_loop().call_later(
            self.HEARTBEAT_PERIOD_IN_SEC, self._heartbeat)


class Server:

    def __init__(self, host, port=12345):
        self.event_loop = asyncio.get_event_loop()
        self.host = host
        self.port = port

        self.protocol_coroutine = self.event_loop.create_server(
            ServerProtocol,
            host=self.host,
            port=self.port
        )
        self.server = self.event_loop.run_until_complete(
            self.protocol_coroutine)

    def run_forever(self):

        self.event_loop.run_forever()
        server.close()
        self.event_loop.run_until_complete(server.wait_closed())
        self.event_loop.close()


if __name__ == '__main__':
    Server("localhost").run_forever()
    print("Server Terminated.")
