from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from . import openConnections


class PrometheusWebsocket(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def websocket_connect(self, message):
        openConnections.open_connections += 1
        super().websocket_connect(message)

    def websocket_disconnect(self, message):
        openConnections.open_connections -= 1
        super().websocket_disconnect(message)


class AsyncPrometheusWebsocket(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def websocket_connect(self, message):
        openConnections.open_connections += 1
        await super().websocket_connect(message)

    async def websocket_disconnect(self, message):
        openConnections.open_connections -= 1
        await super().websocket_disconnect(message)
