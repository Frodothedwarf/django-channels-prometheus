from django.urls import path, include
from channels_prometheus import urls as channels_prometheus_urls

urlpatterns = [
    path('metrics/', include(channels_prometheus_urls))
]