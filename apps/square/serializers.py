from rest_framework import serializers

from apps.media.serializers import FileSerializer
from .models import Collection, Issues, Reply, ThumbsUp


class IssuesSerializer(serializers.ModelSerializer):
    collections = serializers.SerializerMethodField()
    collection_count = serializers.SerializerMethodField()
    thumbs_up = serializers.SerializerMethodField()
    thumbs_up_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    # 发布者
    publisher_id = serializers.CharField(
        read_only=True, source="publisher.id")
    publisher_name = serializers.CharField(
        read_only=True, source="publisher.username")

    media_detial = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        # fields = "__all__"
        exclude = ["publisher", ]
        extra_kwargs = {
            "id": {"required": False, "allow_null": True},
            "title": {"required": True, "allow_null": False},
            "publisher": {"required": False, "allow_null": True},
            "medias": {"required": False, "allow_null": True},
            "status": {"required": False},
            "content": {"required": False},
        }

    def get_collections(self, issues):
        collections = Collection.objects.filter(issues__id=issues.id)
        return CollectionSerializer(collections, many=True).data

    def get_thumbs_up(self, issues):
        thumbs_up = ThumbsUp.objects.filter(issues__id=issues.id)
        return ThumbsUpSerializer(thumbs_up, many=True).data

    def get_replies(self, issues):
        replies = Reply.logic_objects.filter(issues__id=issues.id)
        return ReplySerializer(replies, many=True).data

    def get_media_detial(self, issues):
        fs = issues.medias
        return FileSerializer(fs, many=True).data

    def get_collection_count(self, issues):
        count = Collection.objects.filter(issues__id=issues.id).count()
        return count

    def get_thumbs_up_count(self, issues):
        count = ThumbsUp.objects.filter(issues__id=issues.id).count()
        return count

    def get_reply_count(self, issues):
        count = Reply.logic_objects.filter(issues__id=issues.id).count()
        return count


class CollectionSerializer(serializers.ModelSerializer):

    publisher_id = serializers.CharField(read_only=True, source="publisher.id")
    publisher_name = serializers.CharField(
        read_only=True, source="publisher.username")

    class Meta:
        model = Collection
        exclude = ["publisher", ]


class ThumbsUpSerializer(serializers.ModelSerializer):

    publisher_id = serializers.CharField(read_only=True, source="publisher.id")
    publisher_name = serializers.CharField(
        read_only=True, source="publisher.username")

    class Meta:
        model = ThumbsUp
        exclude = ["publisher", ]


class ReplySerializer(serializers.ModelSerializer):
    thumbs_up = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    media_detial = serializers.SerializerMethodField()

    publisher_id = serializers.CharField(
        read_only=True, source="publisher.id")
    publisher_name = serializers.CharField(
        read_only=True, source="publisher.username")

    class Meta:
        model = Reply
        exclude = ["publisher", ]
        extra_kwargs = {
            "id": {"required": False, "allow_null": True},
            "medias": {"required": False, "allow_null": True},
        }

    def get_thumbs_up(self, reply):
        thumbs_up = ThumbsUp.objects.filter(reply__id=reply.id)
        return ThumbsUpSerializer(thumbs_up, many=True).data

    def get_replies(self, reply):
        replies = Reply.logic_objects.filter(reply__id=reply.id)
        return ReplySerializer(replies, many=True).data

    def get_media_detial(self, reply):
        fs = reply.medias
        return FileSerializer(fs, many=True).data
