from django.urls import include, path
from rest_framework.routers import DefaultRouter

from booking.services.payment.payment_webhook import StripeWebhookView
from booking.services.payment.yoomany_webhook import YooMoneyWebhookView

from .views import BookingViewSet, get_apartment_availability, payment_cancel, payment_success

router = DefaultRouter()
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("available_dates/<int:apartment_id>/", get_apartment_availability, name="available_dates"),
    path("webhook/stripe/", StripeWebhookView.as_view(), name="stripe_webhook"),
    path("webhook/yookasa/", YooMoneyWebhookView.as_view(), name="yookasa_webhook"),
    path("payment/success/<int:booking_id>/", payment_success, name="payment_success"),
    path("payment/cancel/", payment_cancel, name="payment_cancel"),
]
