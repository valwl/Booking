from datetime import timedelta
from decimal import Decimal


def calculate_booking_price(*, apartment, checkin, checkout) -> Decimal:
    days = (checkout - checkin).days
    if days <= 0:
        raise ValueError("checkout must be after checkin")
    weekday_days = sum(1 for i in range(days) if (checkin + timedelta(days=i)).weekday() < 5)
    weekend_days = days - weekday_days
    return Decimal(weekday_days) * apartment.base_price + Decimal(weekend_days) * apartment.weekend_price
