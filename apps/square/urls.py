from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from . import views

app_name = "square"

router_v1 = routers.SimpleRouter()
router_v1.register(r'issues', views.IssuesViewSet, basename='issues')

urlpatterns = [
    url(r'', include((router_v1.urls, "square"), namespace='square_v1')),
]
