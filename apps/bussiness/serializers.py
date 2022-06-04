from rest_framework import serializers

from apps.bussiness.models import Category, Collection, Share, Tag, ThumbUp
from django.contrib.contenttypes.models import ContentType


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


class ThumbUpSerializer(GenericSerializer):
    tper_id = serializers.CharField(
        read_only=True, source="tper.id")
    tper_name = serializers.CharField(
        read_only=True, source="tper.username")

    class Meta:
        model = ThumbUp
        fields = "__all__"


class ShareSerializer(GenericSerializer):
    class Meta:
        model = Share
        fields = "__all__"

    sharer_id = serializers.CharField(
        read_only=True, source="sharer.id")
    sharer_name = serializers.CharField(
        read_only=True, source="sharer.username")


class CollectionSerializer(GenericSerializer):
    class Meta:
        model = Collection
        fields = "__all__"

    collecter_id = serializers.CharField(
        read_only=True, source="collecter.id")
    collecter_name = serializers.CharField(
        read_only=True, source="collecter.username")
