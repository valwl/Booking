from django.contrib import admin

from .models.availability import UnavailableDate
from .models.booking import Booking
from .models.payment import Payment

admin.site.register(Booking)
admin.site.register(UnavailableDate)
admin.site.register(Payment)
