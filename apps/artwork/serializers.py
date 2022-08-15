from rest_framework import serializers

from apps.artwork.models import Art, Author
from apps.media.serializers import FileSerializer


class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = "__all__"
        extra_kwargs = {
            "id": {"required": False, "allow_null": True},
            "title": {"required": True, "allow_null": False},
            "medias": {"required": False, "allow_null": True},
            "author": {"required": False, "allow_null": True},
        }

    media_detail = serializers.SerializerMethodField()
    author_name = serializers.CharField(read_only=True, source="author.name")
    author_id = serializers.CharField(read_only=True, source="author.id")

    def get_media_detail(self, art):
        fs = art.medias
        return FileSerializer(fs, many=True).data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

