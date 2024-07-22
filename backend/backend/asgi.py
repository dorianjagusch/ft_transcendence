"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from backend.urls import websocket_urlpatterns

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Define the ASGI application that will route requests to different protocols (remember to change to https and wss later)
application = ProtocolTypeRouter({
    # HTTP protocol routing
    "http": django_asgi_app,
    
    # WebSocket protocol routing
    "websocket": URLRouter(websocket_urlpatterns),
})
