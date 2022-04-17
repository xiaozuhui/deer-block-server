from . import views
from rest_framework import routers
from django.conf.urls import url, include

router_v1 = routers.SimpleRouter()
router_v1.register(r'profile', views.ProfileViewSet)


urlpatterns = [
    url(r'', include((router_v1.urls, "users"), namespace='user_v1')),
]
