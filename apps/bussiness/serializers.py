from rest_framework import serializers

from apps.bussiness.models import Category, Collection, Share, Tag, ThumbUp
from django.contrib.contenttypes.models import ContentType


class TagSerializer(serializers.ModelSerializer):
    """标签是用户能够自己创建的
    """
    class Meta:
        model = Tag
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """分类全部是系统内建
    """
    class Meta:
        model = Category
        fields = "__all__"


class ThumbUpSerializer(serializers.ModelSerializer):

    content_type_app = serializers.SerializerMethodField()
    content_type_model = serializers.SerializerMethodField()

    class Meta:
        model = ThumbUp
        fields = "__all__"

    def get_content_type_app(self, tp):
        return tp.content_type.app_label

    def get_content_type_model(self, tp):
        return tp.content_type.model


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
