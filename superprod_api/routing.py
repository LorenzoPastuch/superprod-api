from django.urls import path
from .consumers import PCPConsumer

websocket_urlpatterns = [
    path('ws/pcp/', PCPConsumer.as_asgi()),
]
