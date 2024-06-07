import json

from channels_prometheus.websocket import AsyncPrometheusWebsocket, PrometheusWebsocket

class AsyncTestConsumer(AsyncPrometheusWebsocket):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

class TestConsumer(PrometheusWebsocket):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

TestConsumer.__test__ = False