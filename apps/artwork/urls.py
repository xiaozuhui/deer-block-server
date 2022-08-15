from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.artwork.views import ArtViewSet, AuthorViewSet

app_name = "artwork"

route_v1 = routers.SimpleRouter()
route_v1.register(r'art', ArtViewSet)
route_v1.register(r'author', AuthorViewSet)

urlpatterns = [
    url(r'', include((route_v1.urls, "artwork"), namespace='artwork_v1')),
]
