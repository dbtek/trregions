from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from regions.models import City, District
from regions.serializers import CitySerializer, DistrictSerializer
from rest_framework import filters


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ('city',)
    search_fields = ('title',)
