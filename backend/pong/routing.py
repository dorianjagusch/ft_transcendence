# pong/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('pong/<int:match_id>', consumers.PongConsumer.as_asgi()),
]
