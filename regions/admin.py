from django.contrib import admin
from django.contrib.admin import ModelAdmin
from regions.models import City, District, Neighborhood


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ('title',)


@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = ('title', 'city')


@admin.register(Neighborhood)
class NeighborhoodAdmin(ModelAdmin):
    list_display = ('title', 'district', 'city')

    list_filter = ('district__city', 'district', )

    def city(self, obj):
        return obj.district.city
