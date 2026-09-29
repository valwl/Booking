from django.db.models import Prefetch

from apartments.models.apartments import Apartment



def get_apartment_detail(*, apartment_id: int):
    return (
        Apartment.objects.select_related("user", "location")
        .get(id=apartment_id)
    )


def get_user_apartment_list(user):
    return Apartment.objects.filter(user=user)
