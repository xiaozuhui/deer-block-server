from rest_framework.viewsets import ModelViewSet

from apps.media import models
from apps.media.serializers import FileSerializer


class FileModelViewSet(ModelViewSet):
    # 正则uuid
    # lookup_value_regex = "[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}"
    ordering_fields = ("upload_time",)
    queryset = models.File.objects.all()
    serializer_class = FileSerializer
