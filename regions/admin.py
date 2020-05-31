from django.contrib import admin
from django.contrib.admin import ModelAdmin
from regions.models import City, District


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ('title',)


@admin.register(District)
class District(ModelAdmin):
    list_display = ('title', 'city')