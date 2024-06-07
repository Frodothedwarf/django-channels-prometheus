from django.test import Client, TestCase
from channels.testing import WebsocketCommunicator, HttpCommunicator
from .consumers import AsyncTestConsumer, TestConsumer
import pytest
from django.test import Client
from asgiref.sync import sync_to_async

class TestChannelsPrometheus(TestCase):
    @pytest.mark.asyncio
    async def test_async_websocket_connection(self):
        self.websocketCommunicator1 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        connected, subprotocol = await self.websocketCommunicator1.connect()
        assert connected

        await self.websocketCommunicator1.disconnect()

    @pytest.mark.asyncio
    async def test_async_websocket_counter(self):
        self.websocketCommunicator1 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator2 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator3 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator4 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator5 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator6 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator7 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator8 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator9 = WebsocketCommunicator(AsyncTestConsumer.as_asgi(), "/ws/test/")
        await self.websocketCommunicator1.connect()
        await self.websocketCommunicator2.connect()
        await self.websocketCommunicator3.connect()
        await self.websocketCommunicator4.connect()
        await self.websocketCommunicator5.connect()
        await self.websocketCommunicator6.connect()
        await self.websocketCommunicator7.connect()
        await self.websocketCommunicator8.connect()
        await self.websocketCommunicator9.connect()

        client = Client()
        response = client.get("/metrics/")
        self.assertContains(response, "9.0")

        await self.websocketCommunicator1.disconnect()
        await self.websocketCommunicator2.disconnect()
        await self.websocketCommunicator3.disconnect()
        await self.websocketCommunicator4.disconnect()
        await self.websocketCommunicator5.disconnect()
        await self.websocketCommunicator6.disconnect()
        await self.websocketCommunicator7.disconnect()
        await self.websocketCommunicator8.disconnect()
        await self.websocketCommunicator9.disconnect()
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        self.websocketCommunicator1 = WebsocketCommunicator(TestConsumer.as_asgi(), "/ws/test/")
        connected, subprotocol = await self.websocketCommunicator1.connect()
        assert connected

        await self.websocketCommunicator1.disconnect()

    @pytest.mark.asyncio
    async def test_websocket_counter(self):
        self.websocketCommunicator1 = WebsocketCommunicator(TestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator2 = WebsocketCommunicator(TestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator3 = WebsocketCommunicator(TestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator4 = WebsocketCommunicator(TestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator5 = WebsocketCommunicator(TestConsumer.as_asgi(), "/ws/test/")
        self.websocketCommunicator6 = WebsocketCommunicator(TestConsumer.as_asgi(), "/ws/test/")
        await self.websocketCommunicator1.connect()
        await self.websocketCommunicator2.connect()
        await self.websocketCommunicator3.connect()
        await self.websocketCommunicator4.connect()
        await self.websocketCommunicator5.connect()
        await self.websocketCommunicator6.connect()

        client = Client()
        response = client.get("/metrics/")
        self.assertContains(response, "6.0")

        await self.websocketCommunicator1.disconnect()
        await self.websocketCommunicator2.disconnect()
        await self.websocketCommunicator3.disconnect()
        await self.websocketCommunicator4.disconnect()
        await self.websocketCommunicator5.disconnect()
        await self.websocketCommunicator6.disconnect()
        
