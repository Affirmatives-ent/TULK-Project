# myproject/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing  # Import your routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Add your WebSocket routing here
    "websocket": URLRouter(routing.websocket_urlpatterns),
})
