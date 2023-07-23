# routing.py
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from chat.consumers import ChatConsumer
from accounts.consumers import OnlineStatusConsumer

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/chat/<uuid:user_id>/", ChatConsumer.as_asgi()),
                    path("ws/online-status/", OnlineStatusConsumer.as_asgi()),
                ]
            )
        ),
    }
)
