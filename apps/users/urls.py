from django.conf.urls import url, include
from rest_framework import routers

from . import views

router_v1 = routers.SimpleRouter()
router_v1.register(r'user', views.UserViewSet)
router_v1.register(r'profile', views.ProfileViewSet)

urlpatterns = [
    url(r'', include((router_v1.urls, "users"), namespace='user_v1')),
]
