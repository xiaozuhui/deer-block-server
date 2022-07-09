from rest_framework import serializers

from apps.bussiness.models import Category, Collection, Share, Tag, ThumbUp, Comment, Message


class TagSerializer(serializers.ModelSerializer):
    """标签是用户能够自己创建的
    """

    class Meta:
        model = Tag
        fields = "__all__"

    # 发布者
    user_id = serializers.CharField(
        read_only=True, source="user.id")
    user_name = serializers.CharField(
        read_only=True, source="user.username")


class CategorySerializer(serializers.ModelSerializer):
    """分类全部是系统内建
    """

    class Meta:
        model = Category
        fields = "__all__"


class GenericSerializer(serializers.ModelSerializer):
    content_type_app = serializers.SerializerMethodField()
    content_type_model = serializers.SerializerMethodField()

    def get_content_type_app(self, obj):
        return obj.content_type.app_label

    def get_content_type_model(self, obj):
        return obj.content_type.model

    user_id = serializers.CharField(read_only=True, source="user.id")
    username = serializers.CharField(read_only=True, source="user.username")


class ThumbUpSerializer(GenericSerializer):
    class Meta:
        model = ThumbUp
        fields = "__all__"


class ShareSerializer(GenericSerializer):
    class Meta:
        model = Share
        fields = "__all__"


class CollectionSerializer(GenericSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class CommentSerializer(GenericSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    # 当前用户是否点赞
    is_thumbs_up = serializers.SerializerMethodField()
    # 该评论的点赞次数
    thumbs_up_count = serializers.SerializerMethodField()

    def get_thumbs_up_count(self, comment):
        count = ThumbUp.get_count(comment)
        return count

    def get_is_thumbs_up(self, comment):
        """
        当前用户对于这个issues对象是否点赞
        """
        if not self.request.user:
            return False
        tps = comment.get_thumb_up(self.request.user)
        if tps and len(tps) == 1:
            return True
        return False


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
