from django.conf.urls import url
from django.urls import include
from apps.bussiness.views import TagViewSet

from rest_framework import routers

app_name = "bussiness"

route_v1 = routers.SimpleRouter()
route_v1.register(r'buss', TagViewSet)

urlpatterns = [
    url(r'', include((route_v1.urls, "buss"), namespace='bussiness_v1')),
]
