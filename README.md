[![codecov](https://codecov.io/gh/Frodothedwarf/django-channels-prometheus/branch/main/graph/badge.svg?token=UDYMWPIGRR)](https://codecov.io/gh/Frodothedwarf/django-channels-prometheus) [![CI](https://github.com/Frodothedwarf/django-channels-prometheus/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/Frodothedwarf/django-channels-prometheus/actions/workflows/ci.yaml)

# Django Channels Prometheus

This project was created with the simplest problem in mind, know how many devices are connected to a websocket, and export that metric to a Prometheus endpoint. Currently the only feature this project has is counting the numbers of open connections to a given websocket inside Django Channels.

You can either choose to enable logging for multiple consumers or just one.

Currently there are plans for naming the websockets and outputting different stats, for different websockets.

At the moment all consumers will count towards the same metric.

## Documentation

Firstly you need to have Django Channels installed, and configured correctly. The project is currently only tested with Daphne and Uvicorn, but other ASGI web servers can be added if the community deems so.

Then install the package via pip:

```
pip install django-channels-prometheus
```

Inside your installed apps in settings.py add the package:

```
INSTALLED_APPS = [
    ...
    'channels_prometheus',
    ...
]
```

Inside your consumer you will need to replace the current `WebsocketConsumer`or `AsyncWebsocketConsumer` with the drop in replacement `PrometheusWebsocket` or `AsyncPrometheusWebsocket` like so:

```
import json

from channels_prometheus.websocket import AsyncPrometheusWebsocket

class ChatConsumer(AsyncPrometheusWebsocket):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
```

After that you will need to add the urls to the Prometheus endpoint to your projects urls like so:

```
from django.urls import path, include
from channels_prometheus import urls as channels_prometheus_urls
from . import views

urlpatterns = [
    path('', views.home),
    path('metrics/', include(channels_prometheus_urls))
]
```

Then make sure that you are pointing to the Djangos ASGI version inside your `asgi.py`:

```
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from tests.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
```

When all of that is configured you will be able to find your endpoint metrics at the defined url route.

## TODO

* Create documentation
* Seperate different consumers to their own metrics.

## Contributing

Contributions are always welcome!

Read through the `contributing.md` to know how to get started.

Please adhere to this project's `code of conduct`.


## License

[MIT](https://choosealicense.com/licenses/mit/)

