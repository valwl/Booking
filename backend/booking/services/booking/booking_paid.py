from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from booking.models.booking import Booking
from booking.selectors.booking_selectors import get_booking_by_id

channel_layer = get_channel_layer()


def mark_booking_as_paid(booking_id):
    booking = get_booking_by_id(booking_id)
    if booking.status != Booking.STATUS_PENDING:
        return
    booking.status = Booking.STATUS_PAID
    booking.save(update_fields=["status"])
    async_to_sync(channel_layer.group_send)(
        f"booking_{booking.id}",
        {
            "type": "booking_event",
            "payload": {
                "type": "payment_success",
                "status": "paid",
                "booking_id": booking.id,
            },
        },
    )
