import os
from django.conf import settings
from django.core.management.base import BaseCommand
import xlrd

from regions.models import City, District, Neighborhood


class DistrictToSave:
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title')
        self.city = kwargs.get('city')
        self.city_id = None


class NeighborhoodToSave:
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title')
        self.district = kwargs.get('district')
        self.city = kwargs.get('city')
        self.district_id = None


class Command(BaseCommand):
    help = 'Import latest Turkey regions data'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='data.xlsx')

    def handle(self, *args, **options):
        try:
            wb = xlrd.open_workbook(os.path.join(settings.BASE_DIR, options['file']))
        except FileNotFoundError:
            print("Couldn't open file \"%s\", please download it from http://postakodu.ptt.gov.tr/Dosyalar/pk_list.zip" %
                  options['file'])
            return

        sheet = wb.sheet_by_index(0)

        neighborhoods = []
        districts = []
        cities = []

        if sheet.ncols != 5:
            raise Exception('Number of cols should be 5. Please check input file.')

        print('Reading data...')

        for i in range(1, sheet.nrows):
            city = sheet.cell_value(i, 0).strip()
            district = DistrictToSave(title=sheet.cell_value(i, 1).strip(), city=city)
            neighborhood = NeighborhoodToSave(title=sheet.cell_value(i, 3).strip(), district=district.title, city=city)

            if not any(x == city for x in cities):
                cities.append(city)
            if not any(x.title == district.title and x.city == district.city for x in districts):
                districts.append(district)

            # since neighborhoods is unique append it without check
            neighborhoods.append(neighborhood)

        print('Checking for %d cities; %d districts; %d neighborhoods.' % (
            len(cities), len(districts), len(neighborhoods)))

        print('Importing missing records...')
        c = 0
        for city in cities:
            try:
                City.objects.get(title=city)
            except City.DoesNotExist:
                c += 1
                City.objects.create(title=city)

        print('Imported %d cities.' % c)

        d = 0
        for district in districts:
            try:
                saved_city = City.objects.get(title=district.city)
                district.city_id = saved_city.id
            except City.DoesNotExist:
                print('Skip saving district %s, since %s is not found.' % (district.title, district.city))
                continue

            try:
                District.objects.get(title=district.title, city__title=district.city)
            except District.DoesNotExist:
                d += 1
                District.objects.create(title=district.title, city_id=district.city_id)

        print('Imported %d districts.' % d)

        n = 0
        for neighborhood in neighborhoods:
            try:
                saved_district = District.objects.get(title__exact=neighborhood.district, city__title=neighborhood.city)
                neighborhood.district_id = saved_district.id
            except District.DoesNotExist:
                print('Skip saving neighborhood %s, since "%s/%s" is not found.' % (
                    neighborhood.title, neighborhood.city, neighborhood.district))
                continue

            try:
                Neighborhood.objects.get(title=neighborhood.title,
                                         district__title=neighborhood.district,
                                         district__city__title=neighborhood.city)
            except Neighborhood.DoesNotExist:
                n += 1
                Neighborhood.objects.create(title=neighborhood.title, district_id=neighborhood.district_id)

        print('Imported %d neighborhoods.' % n)
        print('Finished import.')
