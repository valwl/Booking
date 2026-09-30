from rest_framework import serializers

from apartments.models.apartments import Apartment
from booking.models.booking import Booking


class BookingCreateSerializer(serializers.Serializer):
    apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all())
    checkin_day = serializers.DateField()
    checkout_day = serializers.DateField()
    guests = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if data["checkin_day"] >= data["checkout_day"]:
            raise serializers.ValidationError("Checkout must be after checkin")
        return data


class BookingListSerializer(serializers.ModelSerializer):
    apartment_title = serializers.CharField(source="apartment.title", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "apartment_title",
            "apartment",
            "checkin_day",
            "checkout_day",
            "total_price",
            "status",
            "create",
        )


class BookingDetailSerializer(serializers.ModelSerializer):
    apartment = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ["id", "apartment", "checkin_day", "checkout_day", "total_price", "status", "create"]


class AvailabilitySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    available_dates = serializers.ListField(child=serializers.DateField())
    blocked_dates = serializers.ListField(child=serializers.DateField())
