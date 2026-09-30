import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.events.yoomoney_event_handler import handle_yoomoney_event

logger = logging.getLogger(__name__)


class YooMoneyWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        logger.info("YooMoney webhook received: %s", request.data)

        try:
            handle_yoomoney_event(request.data)

        except Exception:
            logger.exception("YooMoney webhook processing failed")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
