from django.db import models


class Locations(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.pk}"


class LocationImg(models.Model):
    img = models.ImageField(upload_to="images/locations/", null=True, blank=True)
    location = models.ForeignKey(Locations, related_name="images", on_delete=models.CASCADE)
