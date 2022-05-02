from django.conf.urls import url
from django.urls import include

from apps.media import views
from rest_framework import routers

app_name = "medias"

route_v1 = routers.SimpleRouter()
route_v1.register(r'file', views.FileModelViewSet)

urlpatterns = [
    url(r'', include((route_v1.urls, "medias"), namespace='medias_v1')),
]
