from channels.generic.websocket import AsyncWebsocketConsumer
from channels_prometheus.decorators import ensure_prometheus_connect_async

@ensure_prometheus_connect_async
class AsyncTestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

@ensure_prometheus_connect_async
class AsyncTestConsumerWithoutDisconnect(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
@ensure_prometheus_connect_async
class AsyncTestExceptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        try:
            raise Exception("Test")
        except Exception:
            await self.close()
        
    async def disconnect(self, close_code):
        pass

@ensure_prometheus_connect_async
class AsyncTestExceptionBeforeAcceptConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            raise Exception("Test")
        except Exception:
            await self.close()
        
        await self.accept()

    async def disconnect(self, close_code):
        pass
