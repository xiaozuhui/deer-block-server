from rest_framework import serializers
from apps.bussiness.models import Collection, Share, ThumbUp
from apps.bussiness.serializers import CollectionSerializer, ShareSerializer, ThumbUpSerializer

from apps.media.serializers import FileSerializer
from .models import Issues, Reply


class IssuesSerializer(serializers.ModelSerializer):
    collections = serializers.SerializerMethodField()
    collection_count = serializers.SerializerMethodField()
    thumbs_up = serializers.SerializerMethodField()
    thumbs_up_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()

    # 发布者
    publisher_id = serializers.CharField(
        read_only=True, source="publisher.id")
    publisher_name = serializers.CharField(
        read_only=True, source="publisher.username")

    media_detail = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        fields = "__all__"
        extra_kwargs = {
            "id": {"required": False, "allow_null": True},
            "title": {"required": True, "allow_null": False},
            "publisher": {"required": False, "allow_null": True},
            "medias": {"required": False, "allow_null": True},
            "status": {"required": False},
            "content": {"required": False},
            "origin": {"required": False, "allow_null": True},
            "version": {"required": False, "allow_null": True},
            "tags": {"required": False, "allow_null": True},
            "categories": {"required": False, "allow_null": True},
        }

    def get_collections(self, issues):
        collections = Collection.get_instances(issues)
        # collections = Collection.logic_objects.filter(issues__id=issues.id)
        return CollectionSerializer(collections, many=True).data

    def get_thumbs_up(self, issues):
        thumbs_ups = ThumbUp.get_instances(issues)
        # thumbs_up = ThumbUp.logic_objects.filter(issues__id=issues.id)
        return ThumbUpSerializer(thumbs_ups, many=True).data

    def get_replies(self, issues):
        replies = Reply.logic_objects.filter(issues__id=issues.id)
        return ReplySerializer(replies, many=True).data

    def get_media_detail(self, issues):
        fs = issues.medias
        return FileSerializer(fs, many=True).data

    def get_collection_count(self, issues):
        # count = Collection.logic_objects.filter(issues__id=issues.id).count()
        count = Collection.get_count(issues)
        return count

    def get_thumbs_up_count(self, issues):
        # count = ThumbUp.logic_objects.filter(issues__id=issues.id).count()
        count = ThumbUp.get_count(issues)
        return count

    def get_reply_count(self, issues):
        count = Reply.logic_objects.filter(issues__id=issues.id).count()
        return count

    def get_shares(self, issues):
        # sahres = Share.logic_objects.filter(issues__id=issues.id)
        sahres = Share.get_instances(issues)
        return ShareSerializer(sahres, many=True).data

    def get_share_count(self, issues):
        # count = Share.logic_objects.filter(issues__id=issues.id).count()
        count = Share.get_count(issues)
        return count


class ReplySerializer(serializers.ModelSerializer):
    thumbs_up = serializers.SerializerMethodField()
    thumbs_up_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    media_detial = serializers.SerializerMethodField()

    publisher_id = serializers.CharField(
        read_only=True, source="publisher.id")
    publisher_name = serializers.CharField(
        read_only=True, source="publisher.username")

    class Meta:
        model = Reply
        fields = "__all__"
        extra_kwargs = {
            "id": {"required": False, "allow_null": True},
            "medias": {"required": False, "allow_null": True},
            "publisher": {"required": False, "allow_null": True},
        }

    def get_thumbs_up(self, reply):
        thumbs_ups = ThumbUp.get_instances(reply)
        return ThumbUpSerializer(thumbs_ups, many=True).data

    def get_thumbs_up_count(self, reply):
        count = ThumbUp.get_count(reply)
        return count

    def get_replies(self, reply):
        replies = Reply.logic_objects.filter(reply__id=reply.id)
        return ReplySerializer(replies, many=True).data

    def get_media_detial(self, reply):
        fs = reply.medias
        return FileSerializer(fs, many=True).data
