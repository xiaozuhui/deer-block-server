from django.contrib import admin

from apps.media.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    def file_size(self, file):
        file_size = file.file.size
        if file_size > 1024 * 1024:
            return "{} MB".format(file_size // (1024 * 1024))
        elif file_size > 1024:
            return "{} KB".format(file_size // 1024)
        else:
            return "{} B".format(file_size)

    file_size.short_description = "文件大小"

    list_display = ("id", "title", "file", "uploader",
                    "file_type", "file_size", "upload_time",
                    "is_active", "is_private", "sequence")
    list_filter = ('uploader', 'file_type', 'upload_time')
    list_per_page = 40
    ordering = ('upload_time',)
