import pytest
from channels.testing import WebsocketCommunicator
from django.test import Client, TestCase

from .consumers_async import AsyncTestConsumer, AsyncTestConsumerWithoutDisconnect, AsyncTestExceptionConsumer, AsyncTestExceptionBeforeAcceptConsumer
from .test_helpers import websocket_creator, websocket_connector

class TestAsyncWebSocketConsumer(TestCase):
    @pytest.mark.asyncio
    async def test_async_websocket_connection(self):
        self.websocketCommunicator1 = WebsocketCommunicator(
            AsyncTestConsumer.as_asgi(), "/ws/test/"
        )
        connected, subprotocol = await self.websocketCommunicator1.connect()
        assert connected

        await self.websocketCommunicator1.disconnect()

    @pytest.mark.asyncio
    async def test_async_websocket_counter(self):
        websockets = websocket_creator(AsyncTestConsumer, "/ws/test/", 9)
        websockets = await websocket_connector(websockets, True)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "9.0")

        websockets = await websocket_connector(websockets, False)
    
    @pytest.mark.asyncio
    async def test_async_websocket_without_disconnect_counter(self):
        websockets = websocket_creator(AsyncTestConsumerWithoutDisconnect, "/ws/test/", 7)
        websockets = await websocket_connector(websockets, True)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "7.0")

        websockets = await websocket_connector(websockets, False)

    @pytest.mark.asyncio
    async def test_websocket_counter_fail(self):
        websockets = websocket_creator(AsyncTestExceptionConsumer, "/ws/test/fail/", 3)

        # Connect and disconnect is done this way due to the websocket protocol is demanding it to be.
        # Server send close, client acknowledges it and sends goodbye
        websockets = await websocket_connector(websockets, True)
        websockets = await websocket_connector(websockets, False)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "0.0")

    @pytest.mark.asyncio
    async def test_websocket_counter_before_accept_fail(self):
        websockets = websocket_creator(AsyncTestExceptionBeforeAcceptConsumer, "/ws/test/fail/before/", 3)

        # Connect and disconnect is done this way due to the websocket protocol is demanding it to be.
        # Server send close, client acknowledges it and sends goodbye
        websockets = await websocket_connector(websockets, True)
        websockets = await websocket_connector(websockets, False)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "0.0")
