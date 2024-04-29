from django.urls import re_path

from pong import consumers as game_consumers

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<room_name>\w+)/$", game_consumers.GameConsumer.as_asgi())
]