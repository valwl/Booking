from django.contrib.auth import get_user_model
from django.db import models

from .locations import Locations

User = get_user_model()


class Apartment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    weekend_price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}, {self.pk}"


class ApartmentImg(models.Model):
    img = models.ImageField(upload_to="images/apartments/", null=True, blank=True)
    apartment = models.ForeignKey(Apartment, related_name="images", on_delete=models.CASCADE)


class SliderImage(models.Model):
    image = models.ImageField(upload_to="images/slider/", null=True, blank=True)


class PopularApartment(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
