from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from regions.models import City, District, Neighborhood
from regions.serializers import CitySerializer, DistrictSerializer, NeighborhoodSerializer
from rest_framework import filters


class SearchTrFilter(filters.SearchFilter):

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')

        tr_map = {
            'i': 'İ',
            'ç': 'Ç',
            'ğ': 'Ğ',
            'ö': 'Ö',
            'ş': 'Ş',
            'ü': 'Ü'
        }

        for char in tr_map:
            params = params.replace(char, tr_map[char])

        return params.split()


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [SearchTrFilter]
    search_fields = ('title',)


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [SearchTrFilter, DjangoFilterBackend]
    filter_fields = ('city',)
    search_fields = ('title',)


class NeighborhoodsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer
    filter_backends = [SearchTrFilter, DjangoFilterBackend]
    filter_fields = ('district', 'district__city')
    search_fields = ('title',)
