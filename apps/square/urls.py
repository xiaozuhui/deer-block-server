from . import views
from rest_framework import routers
from django.conf.urls import url
from django.urls import include

app_name = "square"

router_v1 = routers.SimpleRouter()
router_v1.register(r'issues', views.IssuesViewSet)
router_v1.register(r'collection', views.CollectionViewSet)
router_v1.register(r'reply', views.ReplyViewSet)
router_v1.register(r'thumb_up', views.ThumbsUpViewSet)


urlpatterns = [
    url(r'', include((router_v1.urls, "square"), namespace='square_v1')),
]
