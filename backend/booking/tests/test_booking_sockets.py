import json

import pytest
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.urls import path
from rest_framework_simplejwt.tokens import AccessToken

# Импортируем твоего консьюмера
from booking.consumers import BookingStatusConsumer

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestBookingWebSockets:
    """Integration test suite for the asynchronous Django Channels layer (Handshake, Heartbeat, Event Delivery)."""


    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        """Initialize test user and generate a live JWT token required by UntypedToken in the consumer."""
        self.user = User.objects.create_user(first_name="ws_user", email="ws@example.com", password="password123")
        self.token = str(AccessToken.for_user(self.user))
        self.booking_id = 42

    async def test_websocket_lifecycle_and_heartbeat(self):
        """Verify successful connection establishment via token and handle Ping-Pong message exchange."""


        application = URLRouter(
            [
                path("ws/booking_status/<int:booking_id>/", BookingStatusConsumer.as_asgi()),
            ]
        )


        path_string = f"ws/booking_status/{self.booking_id}/?token={self.token}"

        communicator = WebsocketCommunicator(application, path_string)


        connected, subprotocol = await communicator.connect()
        assert connected is True, "WebSocket connection was rejected by server"


        await communicator.send_to(text_data=json.dumps({"type": "ping"}))


        response = await communicator.receive_from()
        response_data = json.loads(response)

        assert response_data["type"] == "pong"

        #
        await communicator.disconnect()

    async def test_websocket_broadcast_delivery_on_payment(self):
        """Verify the delivery of real-time payment events broadcasted through the channel layer."""

        application = URLRouter(
            [
                path("ws/booking_status/<int:booking_id>/", BookingStatusConsumer.as_asgi()),
            ]
        )
        path_string = f"ws/booking_status/{self.booking_id}/?token={self.token}"

        communicator = WebsocketCommunicator(application, path_string)
        connected, _ = await communicator.connect()
        assert connected is True


        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f"booking_{self.booking_id}",
            {
                "type": "booking_event",
                "payload": {
                    "type": "payment_success",
                    "status": "paid",
                    "booking_id": self.booking_id,
                },
            },
        )


        server_message = await communicator.receive_from()
        message_data = json.loads(server_message)


        assert message_data["type"] == "payment_success"
        assert message_data["data"]["status"] == "paid"
        assert message_data["data"]["booking_id"] == self.booking_id

        await communicator.disconnect()

    async def test_websocket_no_token_rejected(self):
        """Ensure connection requests without a token are strictly rejected with a 4001 close code."""
        application = URLRouter(
            [
                path("ws/booking_status/<int:booking_id>/", BookingStatusConsumer.as_asgi()),
            ]
        )

        path_string = f"ws/booking_status/{self.booking_id}/"

        communicator = WebsocketCommunicator(application, path_string)
        connected, close_code = await communicator.connect()

        assert connected is False
        assert close_code == 4001
