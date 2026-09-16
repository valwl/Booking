from rest_framework import serializers

from .models.apartments import Apartment, ApartmentImg, Locations, PopularApartment, SliderImage
from .models.locations import LocationImg
from .models.reviews import Review


class ApartmentImgSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = ApartmentImg
        fields = ["img", "id"]

    def get_img(self, obj):
        request = self.context.get("request")
        if obj.img:
            if request:
                absolute_url = f"{request._current_scheme_host}{obj.img.url}"
                return absolute_url
            return obj.img.url
        return None


class ApartmentDetailSerializer(serializers.ModelSerializer):
    images = ApartmentImgSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(source="review_set", many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = [
            "id",
            "title",
            "description",
            "base_price",
            "weekend_price",
            "location",
            "user",
            "images",
            "reviews",
        ]


class ApartmentSerializer(serializers.ModelSerializer):
    images = ApartmentImgSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = ["id", "title", "description", "base_price", "weekend_price", "images", "user", "location"]


class ApartmentCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    weekend_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    location = serializers.PrimaryKeyRelatedField(queryset=Locations.objects.all())
    images = serializers.ListField(child=serializers.ImageField(), required=False)


class LocationsImgSerializers(serializers.ModelSerializer):
    class Meta:
        model = LocationImg
        fields = ["img"]


class LocationSerializer(serializers.ModelSerializer):
    images = LocationsImgSerializers(many=True, read_only=True)

    class Meta:
        model = Locations
        fields = ["id", "name", "description", "images"]


class SliderImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = "__all__"


class PopularApartmentSerializer(serializers.ModelSerializer):
    images = ApartmentImgSerializer(source="apartment.images", many=True, read_only=True)
    id = serializers.IntegerField(source="apartment.id")
    title = serializers.CharField(source="apartment.title")
    description = serializers.CharField(source="apartment.description")
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="apartment.base_price")
    weekend_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="apartment.weekend_price")

    class Meta:
        model = PopularApartment
        fields = ["id", "title", "description", "base_price", "weekend_price", "images"]


class ApartmentUpdateSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    removed_images = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Apartment
        fields = [
            "title",
            "description",
            "base_price",
            "weekend_price",
            "images",
            "removed_images",
        ]

    def get_images(self, instance):
        return [{"id": img.id, "url": img.img.url} for img in instance.images.all()]
