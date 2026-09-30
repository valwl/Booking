from datetime import date, timedelta

from booking.models.availability import UnavailableDate


class AvailabilityService:
    DEFAULT_RANGE_DAYS = 60

    @classmethod
    def is_available(cls, *, apartment, checkin, checkout) -> bool:
        return not UnavailableDate.objects.filter(
            apartment=apartment,
            date__gte=checkin,
            date__lt=checkout,
        ).exists()

    @classmethod
    def block_dates(cls, *, booking):
        current = booking.checkin_day
        while current < booking.checkout_day:
            UnavailableDate.objects.create(apartment=booking.apartment, date=current)
            current += timedelta(days=1)

    @classmethod
    def unblock_dates(cls, *, booking):
        UnavailableDate.objects.filter(
            apartment=booking.apartment,
            date__gte=booking.checkin_day,
            date__lt=booking.checkout_day,
        ).delete()

    @classmethod
    def get_availability(cls, *, apartment, start_date: date | None = None, days: int | None = None) -> dict:
        start_date = start_date or date.today()
        days = days or cls.DEFAULT_RANGE_DAYS
        end_date = start_date + timedelta(days=days)
        all_dates = {start_date + timedelta(days=i) for i in range(days)}

        unavailable_dates = set(
            UnavailableDate.objects.filter(
                apartment=apartment,
                date__gte=start_date,
                date__lt=end_date,
            ).values_list("date", flat=True)
        )

        available_dates = sorted(all_dates - unavailable_dates)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "available_dates": available_dates,
            "blocked_dates": sorted(unavailable_dates),
        }
