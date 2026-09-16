from rest_framework import generics

from apartments.models.apartments import SliderImage
from apartments.serializers import SliderImgSerializer


class ImagesForClientSlider(generics.ListAPIView):
    queryset = SliderImage.objects.all()
    serializer_class = SliderImgSerializer
