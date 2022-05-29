from . import views
from rest_framework import routers
from django.conf.urls import url
from django.urls import include

app_name = "square"

router_v1 = routers.SimpleRouter()
router_v1.register(r'issues', views.IssuesViewSet)
router_v1.register(r'reply', views.ReplyViewSet)


urlpatterns = [
    url(r'', include((router_v1.urls, "square"), namespace='square_v1')),
]
