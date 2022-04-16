from rest_framework.viewsets import ModelViewSet

from file_system import models
from file_system.serializers import MediaSerializer


class MediaModelViewSet(ModelViewSet):
    # 正则uuid
    lookup_value_regex = "[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}"
    ordering_fields = ("upload_time",)
    queryset = models.Media.objects.all()
    serializer_class = MediaSerializer
