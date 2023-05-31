from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chatapp import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r"ws/chat/$", consumers.ChatConsumer.as_asgi()),
    ]),
})