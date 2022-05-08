import http

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.media import models
from apps.media.serializers import FileSerializer


class FileModelViewSet(ModelViewSet):
    """
    上传文件的最低限度的请求参数：
    header使用Bearer的Tooken
    file是文件路径/文件
    curl --location --request POST 'localhost:8080/medias/file/' \
         --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwODY3NDk0LCJpYXQiOjE2NTAyNjI2OTQsImp0aSI6IjRjMzRlYTQ4ZWQzODQwMjdiNDAwZGEzM2ZlOWM0OTY1IiwidXNlcl9pZCI6MX0.UwM6LMc61zDrW5KszqF-DPiBXRfaXHxmaPGHZp1BkYg' \
         --form 'file_type="file"' \
         --form 'file=@"/Users/xuziheng/Documents/T210802221932452070.md"' \
         --form 'is_active="true"' \
         --form 'is_private="false"'
    """
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