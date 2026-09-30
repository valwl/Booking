import json
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class BookingStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from rest_framework_simplejwt.tokens import UntypedToken

        self.booking_id = self.scope["url_route"]["kwargs"]["booking_id"]
        self.group_name = f"booking_{self.booking_id}"

        params = parse_qs(self.scope["query_string"].decode())
        token = params.get("token", [None])[0]

        if token is None:
            print(f"WS reject booking={self.booking_id} reason=no_token")
            await self.close(code=4001)
            return

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError):
            await self.close()
            return

        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        user = await sync_to_async(jwt_auth.get_user)(validated_token)

        self.scope["user"] = user

        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        # TODO: проверить, что user имеет доступ к booking

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("client disconnect form booking", self.booking_id)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            #
            # heartbeat
            #
            if data.get("type") == "ping":
                await self.send(text_data=json.dumps({"type": "pong"}))

        except Exception as exc:
            print("WS receive error", exc)

    async def booking_event(self, event):
        print("booking received ", event)

        await self.send(
            text_data=json.dumps(
                {
                    "type": event["payload"]["type"],
                    "data": event["payload"],
                }
            )
        )
