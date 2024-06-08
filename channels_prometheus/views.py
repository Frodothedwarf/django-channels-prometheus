from django.http import HttpResponse

from . import openConnections


def metrics(request):
    open_connections = openConnections.open_connections
    prometheus_string = f"# HELP open_connections Open websocket connections\n# TYPE open_connections gauge\nopen_connections {open_connections}.0"

    return HttpResponse(content=prometheus_string, content_type="text/plain")
