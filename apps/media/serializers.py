import os

from rest_framework import serializers

import apps.media.models as models


class FileSerializer(serializers.ModelSerializer):
    file_size = serializers.CharField(read_only=True, max_length=20)
    uploader_id = serializers.IntegerField(
        read_only=True, source="uploader.id")
    uploader_name = serializers.CharField(
        read_only=True, source="uploader.username")

    file_list_detail = serializers.SerializerMethodField()

    class Meta:
        model = models.File
        fields = "__all__"
        extra_kwargs = {
            "id": {"required": False, "allow_null": True},
            "file_list": {"required": False, "allow_null": False},
            "uploader": {"required": False, "allow_null": True},
        }

    def get_file_list_detail(self, file):
        fl = file.file_list  # 获取所有的文件的uuid
        files = models.FileStorage.objects.filter(uuid__in=fl)
        return FileStorageSerializer(files, many=True).data


class FileStorageSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_name = serializers.CharField(read_only=True, max_length=50)
    file_size = serializers.CharField(read_only=True, max_length=20)

    class Meta:
        model = models.FileStorage
        fields = "__all__"

        extra_kwargs = {
            "uuid": {"required": False},
            "filename": {"required": True, "allow_null": False},
            "file_type": {"required": False, "allow_null": True},
            "file_extension": {"required": False, "allow_null": True},
            "mime_type": {"required": False, "allow_null": True},
        }

    def get_file_url(self, file):
        url = file.file_url
        minio_ip = os.environ.get("MINIO_IP", "localhost")
        minio_port = os.environ.get(
            "MINIO_PORT", "19090")  # 默认为19090端口，内部端口为9000
        url = url.replace('minio', minio_ip).replace(':9000', ":" + minio_port)
        return url
