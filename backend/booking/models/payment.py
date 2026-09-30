from django.db import models

from .booking import Booking


class Payment(models.Model):
    STATUS_INITIATED = "initiated"
    STATUS_SESSION_CREATED = "session_created"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_EXPIRED = "expired"
    PROVIDER_STRIPE = "Stripe"
    PROVIDER_YOOMONEY = "Yoomoney"

    STATUS_CHOICES = [
        (STATUS_INITIATED, "Initiated"),
        (STATUS_SESSION_CREATED, "Session created"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
        (STATUS_EXPIRED, "Expired"),
    ]

    PROVIDER_CHOICES = [
        (PROVIDER_STRIPE, "stripe"),
        (PROVIDER_YOOMONEY, "yoomoney"),
    ]

    booking = models.ForeignKey(Booking, related_name="payments", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_INITIATED,
    )

    provider = models.CharField(max_length=255, choices=PROVIDER_CHOICES, default=PROVIDER_STRIPE)
    provider_payment_id = models.CharField(max_length=255, null=True, blank=True)
    provider_reference = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"payment fot booking: {self.booking.id}"
