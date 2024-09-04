from channels.generic.websocket import WebsocketConsumer
from channels_prometheus.decorators import ensure_prometheus_connect

@ensure_prometheus_connect
class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

@ensure_prometheus_connect
class TestConsumerWithoutDisconnect(WebsocketConsumer):
    def connect(self):
        self.accept()

@ensure_prometheus_connect
class TestExceptionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        try:
            raise Exception("Test")
        except Exception:
            self.close()

    def disconnect(self, close_code):
        pass

@ensure_prometheus_connect
class TestExceptionBeforeAcceptConsumer(WebsocketConsumer):
    def connect(self):
        try:
            raise Exception("Test")
        except Exception:
            self.close()

        self.accept()

    def disconnect(self, close_code):
        pass

TestConsumer.__test__ = False
TestExceptionConsumer.__test__ = False
TestExceptionBeforeAcceptConsumer.__test__ = False
TestConsumerWithoutDisconnect.__test__ = False