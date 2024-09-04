from channels.testing import WebsocketCommunicator


def websocket_creator(consumer, url, count=1):
    """
    Helper function to tests to create a bunch of websockets and return them in a list.
    """

    websockets = []

    for x in range(count):
        websockets.append(WebsocketCommunicator(consumer.as_asgi(), url))

    return websockets


async def websocket_connector(websockets, connect):
    """
    Helper function to tests to connect a list of websockets.
    """

    for websocket in websockets:
        if connect:
            await websocket.connect()
        else:
            await websocket.disconnect()

    return websockets
