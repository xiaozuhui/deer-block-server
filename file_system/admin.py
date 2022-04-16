from django.contrib import admin


from file_system.models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    def file_size(self, file):
        file_size = file.file.size
        if file_size > 1024 * 1024:
            return "{} MB".format(file_size // (1024 * 1024))
        elif file_size > 1024:
            return "{} KB".format(file_size // 1024)
        else:
            return "{} B".format(file_size)

    file_size.short_description = "文件大小"

    list_display = ("uuid", "title", "file", "uploader_name", "uploader_id",
                    "file_type", "file_size", "upload_time", "is_active", "is_private", "sequence")
    list_filter = ('uploader_name', 'uploader_id', 'file_type', 'upload_time')
    list_per_page = 40
    ordering = ('upload_time',)
