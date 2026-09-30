from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from booking.models.booking import Booking

channel_layer = get_channel_layer()


def mark_booking_payment_failed(*, booking, reason: str = "payment_failed"):
    if booking.status != Booking.STATUS_PENDING:
        return

    booking.status = Booking.STATUS_PAYMENT_FAILED
    booking.payment_error = reason
    booking.save(update_fields=["status", "payment_error"])

    async_to_sync(channel_layer.group_send)(
        f"booking_{booking.id}",
        {
            "type": "booking_event",
            "payload": {
                "type": "payment_failed",
                "status": booking.status,
                "reason": reason,
                "booking_id": booking.id,
            },
        },
    )
