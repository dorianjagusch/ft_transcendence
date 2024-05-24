# pong/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^pong/$', consumers.PongConsumer.as_asgi()),
]
