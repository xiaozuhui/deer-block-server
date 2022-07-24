from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.bussiness.views import TagViewSet, CommentViewSet, MessageViewSet

app_name = "business"

route_v1 = routers.SimpleRouter()
route_v1.register(r'tag', TagViewSet)
route_v1.register(r'comment', CommentViewSet)
route_v1.register(r'notice', MessageViewSet)

urlpatterns = [
    url(r'', include((route_v1.urls, "business"), namespace='business_v1')),
]
