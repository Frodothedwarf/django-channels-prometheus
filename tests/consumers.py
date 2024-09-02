from channels_prometheus.websocket import AsyncPrometheusWebsocket, PrometheusWebsocket


class AsyncTestConsumer(AsyncPrometheusWebsocket):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

class AsyncTestExceptionConsumer(AsyncPrometheusWebsocket):
    async def connect(self):
        await self.accept()
        try:
            raise Exception("Test")
        except:
            await self.websocket_disconnect({"code":1011})
        

    async def disconnect(self, close_code):
        pass

class TestConsumer(PrometheusWebsocket):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass


TestConsumer.__test__ = False
