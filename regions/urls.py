from django.conf.urls import url, include
from rest_framework import routers
from regions import views

router = routers.DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'districts', views.DistrictViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]