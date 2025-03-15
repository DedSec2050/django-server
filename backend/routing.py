from django.urls import re_path
from .consumers import CentralServerConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    re_path(r'ws/server/', CentralServerConsumer.as_asgi()),
    re_path(r"ws/frontend/", CentralServerConsumer.as_asgi()),  # Next.js Frontend
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})


