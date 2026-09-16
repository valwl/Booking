from django.contrib import admin

from .models.apartments import Apartment, ApartmentImg, PopularApartment, SliderImage
from .models.locations import LocationImg, Locations
# from .models.reviews import Review

admin.site.register(Apartment)
admin.site.register(ApartmentImg)
admin.site.register(Locations)
admin.site.register(LocationImg)
admin.site.register(SliderImage)
admin.site.register(PopularApartment)
