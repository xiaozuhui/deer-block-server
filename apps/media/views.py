import http

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.media import models
from apps.media.serializers import FileSerializer


class FileModelViewSet(ModelViewSet):
    ordering_fields = ("upload_time",)
    queryset = models.File.objects.all()
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.__setitem__('uploader', request.user.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=http.HTTPStatus.OK, data=serializer.data, headers=headers)
