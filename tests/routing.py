from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/test/", consumers.AsyncTestConsumer.as_asgi()),
    re_path("ws/test/fail/", consumers.AsyncTestExceptionConsumer.as_asgi()),
]
