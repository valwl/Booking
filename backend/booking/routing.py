from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/booking_status/<int:booking_id>/", consumers.BookingStatusConsumer.as_asgi()),
]
