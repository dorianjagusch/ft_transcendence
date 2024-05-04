from django.urls import path

from . import views
from pong.consumers import PongConsumer, ChatConsumer

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]

#websocket_urlpatterns = [
#    path("new_game/", PongConsumer),
#]