import os

from django.contrib import admin

from apps.media.models import File, FileStorage


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    def file_size(self, file):
        return file.file_size

    file_size.short_description = "文件大小"

    list_display = ("id", "file_list", "uploader",
                    "file_size", "upload_time", "is_active")
    list_filter = ('uploader', 'upload_time')
    list_per_page = 40
    ordering = ('upload_time',)


@admin.register(FileStorage)
class FileStorageAdmin(admin.ModelAdmin):
    def file_size(self, file):
        return file.file_size

    def file_url(self, file):
        url = file.file_url
        minio_ip = os.environ.get("MINIO_IP", "localhost")
        minio_port = os.environ.get(
            "MINIO_PORT", "19090")  # 默认为19090端口，内部端口为9000
        url = url.replace('minio', minio_ip).replace(':9000', ":" + minio_port)
        return url

    file_size.short_description = "文件大小"
    file_url.short_description = "文件地址"

    list_display = ("uuid", "filename", "file",
                    "file_size", "file_url", "is_private", "sequence")
    list_per_page = 40
    ordering = ('sequence',)
