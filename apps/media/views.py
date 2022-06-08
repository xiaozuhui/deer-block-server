import http
import uuid
import logging
import filetype

from apps.base_view import CustomViewBase, JsonResponse

from apps.media import models
from apps.media.serializers import FileSerializer, FileStorageSerializer

logger = logging.getLogger('django')


class FileModelViewSet(CustomViewBase):
    """
    上传文件的最低限度的请求参数：
    header使用Bearer的Tooken
    file是文件路径/文件
    """
    ordering_fields = ("upload_time",)
    queryset = models.File.objects.all()
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        files = request.FILES.getlist('files')
        file_list = []
        for i, f in enumerate(files):
            file_storage = models.FileStorage()
            file_storage.uuid = str(uuid.uuid4())
            file_storage.file = f
            file_storage.filename = f.name
            file_storage.sequence = i
            kind = filetype.guess(f)
            if kind:
                mime = kind.MIME
                extension = kind.EXTENSION
                file_storage.file_extension = extension
                file_storage.mime_type = mime
                mm = mime.split('/')
                if mm and len(mm) > 1:
                    file_storage.file_type = models.FileStorage.pares_file_type(
                        mm[0])
            file_storage.save()
            logger.info("保存file, {}".format(file_storage))
            file_list.append(file_storage.uuid)
        data['uploader'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        f = models.File.objects.filter(id=serializer.data['id']).first()
        if f:
            f.file_list = file_list
            f.save()
            data = FileSerializer(f).data
        headers = self.get_success_headers(data)
        return JsonResponse(status=http.HTTPStatus.OK, data=data, headers=headers)
