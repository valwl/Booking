from django.db import transaction

from apartments.models.reviews import Review


@transaction.atomic
def create_review(*, user, booking, data):
    review = Review.objects.create(user=user, apartment=booking.apartment, booking=booking, **data)

    return review
