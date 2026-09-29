from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apartments.models.apartments import PopularApartment
from apartments.selectors.apartment_queryset import get_apartment_detail, get_user_apartment_list
from apartments.serializers import ApartmentDetailSerializer, ApartmentSerializer, PopularApartmentSerializer


class UserApartmentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        apartments = get_user_apartment_list(user=user)
        serializer = ApartmentSerializer(apartments, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApartmentDetailView(APIView):
    def get(self, request, pk: int):
        apartment = get_apartment_detail(apartment_id=pk)
        serializer = ApartmentDetailSerializer(apartment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularApartmentList(generics.ListAPIView):
    queryset = PopularApartment.objects.all()
    serializer_class = PopularApartmentSerializer
