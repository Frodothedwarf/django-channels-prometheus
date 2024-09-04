import pytest
from channels.testing import WebsocketCommunicator
from django.test import Client, TestCase

from .consumers_sync import (
    TestConsumer,
    TestConsumerWithoutDisconnect,
    TestExceptionBeforeAcceptConsumer,
    TestExceptionConsumer,
)
from .test_helpers import websocket_connector, websocket_creator


class TestSyncWebSocketConsumer(TestCase):
    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        self.websocketCommunicator1 = WebsocketCommunicator(
            TestConsumer.as_asgi(), "/ws/test/"
        )
        connected, subprotocol = await self.websocketCommunicator1.connect()
        assert connected

        await self.websocketCommunicator1.disconnect()

    @pytest.mark.asyncio
    async def test_websocket_counter(self):
        websockets = websocket_creator(TestConsumer, "/ws/test/", 6)
        websockets = await websocket_connector(websockets, True)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "6.0")

        websockets = await websocket_connector(websockets, False)

    @pytest.mark.asyncio
    async def test_websocket_without_disconnect_counter(self):
        websockets = websocket_creator(TestConsumerWithoutDisconnect, "/ws/test/", 4)
        websockets = await websocket_connector(websockets, True)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "4.0")

        websockets = await websocket_connector(websockets, False)

    @pytest.mark.asyncio
    async def test_websocket_counter_fail(self):
        websockets = websocket_creator(TestExceptionConsumer, "/ws/test/fail/", 8)

        # Connect and disconnect is done this way due to the websocket protocol is demanding it to be.
        # Server send close, client acknowledges it and sends goodbye
        websockets = await websocket_connector(websockets, True)
        websockets = await websocket_connector(websockets, False)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "0.0")

    @pytest.mark.asyncio
    async def test_websocket_counter_before_accept_fail(self):
        websockets = websocket_creator(
            TestExceptionBeforeAcceptConsumer, "/ws/test/fail/", 5
        )

        # Connect and disconnect is done this way due to the websocket protocol is demanding it to be.
        # Server send close, client acknowledges it and sends goodbye
        websockets = await websocket_connector(websockets, True)
        websockets = await websocket_connector(websockets, False)

        client = Client()
        response = client.get("/metrics/")

        self.assertContains(response, "0.0")
