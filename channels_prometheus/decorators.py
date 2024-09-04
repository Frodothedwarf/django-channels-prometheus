from . import openConnections


def ensure_prometheus_connect_async(cls):
    """
    Async decorator to Django Channels that wants to enable the count of open connections.
    Usage:
        Use as a decorator on a Django Channels Consumer class.
        \n
        @ensure_prometheus_connect_async\n
        class Consumer(AsyncWebsocketConsumer):\n
            ...
    """

    # Captures the original connect and disconnect from the consumer
    original_connect = cls.connect
    original_disconnect = cls.disconnect

    # Does the count logic and calls the consumer function after
    async def new_connect(self, *args, **kwargs):
        openConnections.open_connections += 1
        await original_connect(self, *args, **kwargs)

    async def new_disconnect(self, *args, **kwargs):
        openConnections.open_connections -= 1
        await original_disconnect(self, *args, **kwargs)

    # Updates the class with the new functions and returns it
    cls.connect = new_connect
    cls.disconnect = new_disconnect
    return cls


# Exactly the same as above, just sync
def ensure_prometheus_connect(cls):
    """
    Sync decorator to Django Channels that wants to enable the count of open connections.
    Usage:
        Use as a decorator on a Django Channels Consumer class.
        \n
        @ensure_prometheus_connect\n
        class Consumer(WebsocketConsumer):\n
            ...
    """

    original_connect = cls.connect
    original_disconnect = cls.disconnect

    def new_connect(self, *args, **kwargs):
        openConnections.open_connections += 1
        original_connect(self, *args, **kwargs)

    def new_disconnect(self, *args, **kwargs):
        openConnections.open_connections -= 1
        original_disconnect(self, *args, **kwargs)

    cls.connect = new_connect
    cls.disconnect = new_disconnect
    return cls
