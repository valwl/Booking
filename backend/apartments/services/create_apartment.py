from django.db import transaction

from apartments.models.apartments import Apartment, ApartmentImg


@transaction.atomic
def create_apartment(*, user, data):
    images = data.pop("images", [])
    apartment = Apartment.objects.create(user=user, **data)

    ApartmentImg.objects.bulk_create([ApartmentImg(apartment=apartment, img=image) for image in images])

    return apartment
