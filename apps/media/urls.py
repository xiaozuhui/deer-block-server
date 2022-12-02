from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.media import views

app_name = "medias"

route_v1 = routers.SimpleRouter()
route_v1.register(r'file', views.FileModelViewSet)

urlpatterns = [
    url(r'', include((route_v1.urls, "medias"), namespace='medias_v1')),
]
