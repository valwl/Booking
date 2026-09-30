from booking.models.booking import Booking


def get_user_bookings(*, user, status=None):
    qs = Booking.objects.filter(user=user)
    if status:
        qs = qs.filter(status=status)
    return qs.select_related("apartment").order_by("create")


def get_booking_by_id(pk):
    return Booking.objects.get(pk=pk)
