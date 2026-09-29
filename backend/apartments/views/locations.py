from rest_framework import generics

from apartments.models.locations import Locations
from apartments.serializers import LocationSerializer


class LocationListView(generics.ListAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer


class LocationDetailView(generics.RetrieveAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer
