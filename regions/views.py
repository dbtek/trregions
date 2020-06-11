from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from regions.models import City, District, Neighborhood
from regions.serializers import CitySerializer, DistrictSerializer, NeighborhoodSerializer
from rest_framework import filters


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ('city',)
    search_fields = ('title',)


class NeighborhoodsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ('district', 'district__city')
    search_fields = ('title',)
