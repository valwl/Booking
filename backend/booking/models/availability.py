from django.db import models

from apartments.models.apartments import Apartment


class UnavailableDate(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ("apartment", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.apartment} - {self.date}"
