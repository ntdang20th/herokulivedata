import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from livedata.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()

ws_patterns = [
    path('ws/sensor/', SensorConsumer.as_asgi()),
]
application = ProtocolTypeRouter({
    'websocket': URLRouter(ws_patterns)
})
