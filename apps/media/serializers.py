from rest_framework import serializers
import apps.media.models as models


class FileSerializer(serializers.ModelSerializer):
    file_url = serializers.CharField(
        read_only=True, max_length=512, source="file_url")
    file_name = serializers.CharField(
        read_only=True, max_length=512, source="file_name")
    file_size = serializers.CharField(
        read_only=True, max_length=20, source="file_size")

    class Meta:
        model = models.File
        fields = "__all__"
