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

    file_size.short_description = "文件大小"

    list_display = ("uuid", "filename", "file",
                    "file_size", "is_private", "sequence")
    list_per_page = 40
    ordering = ('sequence',)
