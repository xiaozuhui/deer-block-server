from django.db import models
from apps.base_model import BaseModel, GenericModel

from apps.users.models import User

"""点赞和收藏，虽然使用了BaseModel，但是不应该使用逻辑删除
而且在使用的时候，也不应该释放出相关的api，而应该从issues等模型处创建或删除
"""


class Share(GenericModel):
    """用于分享的模型，该模型是不是能用于别的app
    """
    sharer = models.ForeignKey(
        User, verbose_name="分享者", on_delete=models.CASCADE)
    share_url = models.URLField(verbose_name="分享链接", default="")
    # 暂定
    share_type = models.CharField(
        max_length=20, verbose_name="分享类型", default="")

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = verbose_name
        db_table = "share"


class Collection(GenericModel):
    """
    收藏，收藏不需要使用逻辑删除
    收藏只能对应动态来收藏，而不能收藏回复
    """
    collecter = models.ForeignKey(
        User, verbose_name="收藏者", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name
        db_table = "collection"


class ThumbUp(GenericModel):
    """
    点赞，点赞不需要逻辑删除
    但是点赞可以对回复进行点赞
    """
    tper = models.ForeignKey(
        User, verbose_name="点赞者", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
        db_table = "thumbs_up"


class Tag(BaseModel):
    label = models.CharField(max_length=10, verbose_name="标签")
    user = models.ForeignKey(User, verbose_name="创建者",
                             on_delete=models.CASCADE)  # 这个只是记录一下是谁创建的这个tag

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        db_table = "tag"


class Category(BaseModel):
    '''
    关于父级分类：
    在创建分类关联的时候，如果选择了二级分类，则需要将一级分类也关联，之后以此类推
    在ser中获取的时候，将实现一颗树
    '''
    label = models.CharField(max_length=100, verbose_name="分类")
    parent_category = models.ForeignKey(
        'Category', verbose_name="父级分类", related_name="parent", on_delete=models.CASCADE)
    level = models.IntegerField(default=0, verbose_name="分级")  # 用于记录

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        db_table = "category"
