from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apartments.models.reviews import Review
from apartments.permissions import IsBookingUser
from apartments.serializers import ReviewCreateInputSerializer
from apartments.services.create_review import create_review
from booking.selectors.booking_selectors import get_booking_by_id


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateInputSerializer
    permission_classes = [IsAuthenticated, IsBookingUser]

    def perform_create(self, serializer):
        booking_id = self.kwargs["booking_id"]
        user = self.request.user

        if Review.objects.filter(user=user, booking_id=booking_id).exists():
            raise ValidationError({"detail": "You can leave only one review for this booking."})
        booking = get_booking_by_id(booking_id)

        create_review(
            user=self.request.user,
            booking=booking,
            data=serializer.validated_data,
        )
