from rest_framework import serializers
import apps.media.models as models


class FileSerializer(serializers.ModelSerializer):
    file_url = serializers.CharField(read_only=True, max_length=512)
    file_name = serializers.CharField(read_only=True, max_length=512)
    file_size = serializers.CharField(read_only=True, max_length=20)
    uploader_id = serializers.IntegerField(read_only=True, source="uploader.id")
    uploader_name = serializers.CharField(read_only=True, source="uploader.username")

    class Meta:
        model = models.File
        fields = "__all__"
