from django.db.models import Prefetch

from apartments.models.apartments import Apartment
from apartments.models.reviews import Review


def get_apartment_detail(*, apartment_id: int):
    return (
        Apartment.objects.select_related("user", "location")
        .prefetch_related("images", Prefetch("review_set", queryset=Review.objects.select_related("user")))
        .get(id=apartment_id)
    )


def get_user_apartment_list(user):
    return Apartment.objects.filter(user=user)
