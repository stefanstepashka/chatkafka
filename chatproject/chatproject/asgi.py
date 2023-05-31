"""
ASGI config for chatproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatproject.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from chatapp import consumers
from django.urls import path


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/<int:chat_id>/", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})



