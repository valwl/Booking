from django.contrib.auth import get_user_model
from django.db import models

from booking.models.booking import Booking

from .apartments import Apartment

User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review", null=True, blank=True)

    def __str__(self):
        return f"review: {self.text} for apartment {self.apartment}"
