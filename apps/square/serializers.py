import logging

from rest_framework import serializers

from apps.business.models import Collection, Share, ThumbUp, Comment
from apps.media.serializers import FileSerializer
from .models import Issues
from ..users.model2 import UserProfile
from ..users.models import User

logger = logging.getLogger(__name__)


class IssuesSerializer(serializers.ModelSerializer):
    collection_count = serializers.SerializerMethodField()
    thumbs_up_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    # 当前账号是否点赞、收藏？
    is_thumbs_up = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()

    # 发布者
    publisher_id = serializers.CharField(
        read_only=True, source="publisher.id")
    publisher_name = serializers.CharField(
        read_only=True, source="publisher.username")
    # 当前用户是否关注了该发布者
    is_publisher_follow = serializers.SerializerMethodField()

    media_detail = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        fields = "__all__"
        extra_kwargs = {
            "id": {"required": False, "allow_null": True},
            "ip": {"required": False, "allow_null": True},
            "title": {"required": False, "allow_null": True},
            "publisher": {"required": False, "allow_null": True},
            "medias": {"required": False, "allow_null": True},
            "status": {"required": False},
            "content": {"required": False, "allow_null": True},
            "tags": {"required": False, "allow_null": True},
            "categories": {"required": False, "allow_null": True},
            "is_video_issues": {"required": False, "allow_null": True},
        }

    def get_media_detail(self, issues):
        fs = issues.medias
        return FileSerializer(fs, many=True).data

    def get_collection_count(self, issues):
        count = Collection.get_count(issues)
        return count

    def get_thumbs_up_count(self, issues):
        count = ThumbUp.get_count(issues)
        return count

    def get_reply_count(self, issues):
        count = Comment.get_count(issues)
        return count

    def get_share_count(self, issues):
        count = Share.get_count(issues)
        return count

    def get_is_thumbs_up(self, issues):
        """
        当前用户对于这个issues对象是否点赞
        """
        logger.info(self.context)
        user_id = self.context.get('user_id', None)
        if not user_id:
            return False
        user = User.logic_objects.filter(id=user_id).first()
        if not user:
            return False
        tps = issues.get_thumb_up(user)
        if tps and len(tps) == 1:
            return True
        return False

    def get_is_collected(self, issues):
        user_id = self.context.get('user_id', None)
        if not user_id:
            return False
        user = User.logic_objects.filter(id=user_id).first()
        if not user:
            return False
        colls = issues.get_collect(user)
        if colls and len(colls) == 1:
            return True
        return False

    def get_is_publisher_follow(self, issues):
        user_id = self.context.get('user_id', None)
        if not user_id:
            logger.error("context上下文没有user_id")
            return False
        user = User.logic_objects.filter(id=user_id).first()
        if not user:
            logger.error(f"user_id[{user_id}]找不到User")
            return False
        publisher = issues.publisher
        user_profile = UserProfile.logic_objects.filter(user__id=user.id).first()
        if not user_profile:
            logger.error(f"user_id[{user_id}]找不到Profile")
            return False
        follows = user_profile.follow.all()
        if publisher not in follows:
            return False
        return True


class IssuesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"

    media_detail = serializers.SerializerMethodField()

    def get_media_detail(self, issues):
        fs = issues.medias
        return FileSerializer(fs, many=True).data
