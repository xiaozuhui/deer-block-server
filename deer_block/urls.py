from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from deer_block import settings
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.users.views import LogoutView
from deer_block import settings

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r"media/", include("apps.media.urls")),
    path(r'user/', include('apps.users.urls')),
    path(r'logout/', LogoutView.as_view(), name='auth_logout'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
