from django.db import models

from apps.base_model import BaseModel, GenericModel
from apps.interfaces.can_comment import CanComment
from apps.interfaces.can_thumbup import CanThumbUp
from apps.media.models import File
from apps.users.models import User
from exceptions.custom_excptions.business_error import BusinessError

"""点赞和收藏，虽然使用了BaseModel，但是不应该使用逻辑删除
而且在使用的时候，也不应该释放出相关的api，而应该从issues等模型处创建或删除
"""


class Share(GenericModel):
    """用于分享的模型，该模型是不是能用于别的app
    """
    user = models.ForeignKey(User, verbose_name="分享者", on_delete=models.CASCADE, related_name="sharer")
    share_url = models.URLField(verbose_name="分享链接", default="")
    # TODO 暂定
    share_type = models.CharField(max_length=20, verbose_name="分享类型", default="")

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = verbose_name
        db_table = "share"


class Collection(GenericModel):
    """
    收藏，收藏不需要使用逻辑删除
    收藏只能对应动态来收藏，而不能收藏回复
    """
    user = models.ForeignKey(User, verbose_name="收藏者", on_delete=models.CASCADE, related_name="collector")

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name
        db_table = "collection"


class ThumbUp(GenericModel):
    """
    点赞，点赞不需要逻辑删除
    但是点赞可以对回复进行点赞
    """
    user = models.ForeignKey(User, verbose_name="点赞者", on_delete=models.CASCADE, related_name="tper")

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
        db_table = "thumbs_up"


class Comment(GenericModel, CanThumbUp, CanComment):
    """
    评论
    1、评论内容
    2、评论者
    3、评论图片，最多三张
    P.S. 评论还可以进行评论，这个怎么写？

    评论模块也可以点赞和评论

    TODO 都应该提示该回复的“父回复”的“回复者”，以及回复中被@的用户
    """
    user = models.ForeignKey(User, verbose_name="评论者", on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField(verbose_name="评论内容", blank=True)
    medias = models.ManyToManyField(File, verbose_name="图片和视频", blank=True)
    # parent_comments = models.ForeignKey('Comment', verbose_name="评论的回复", on_delete=models.DO_NOTHING,
    #                                     related_name="parent_comments", null=True, blank=True)
    ip = models.GenericIPAddressField(verbose_name="评论ip地址", blank=True, null=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        db_table = "comment"

    def create_comment(self, user, content, medias=None, ip=None):
        """
        创建评论

        content: string 评论内容 不可为空
        medias: list of File id 保存的文件id
        parent_comments: 父评论id
        ip: ip地址
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        if not content or not medias:
            # 如果既没有内容又没有图片，则报错
            raise BusinessError.ErrContentEmpty
        comment = Comment.create_instance(self, user=user, content=content, medias=medias, ip=ip)
        return comment

    def delete_comments(self, user):
        """
        删除所有该对象下的所有该用户的评论
        """
        c = Comment.get_instances(self).filter(user__id=user.id)
        if not c:
            raise BusinessError.ErrNoComment
        c.delete()

    def delete_comment(self, comment_id, user):
        """
        删除这个用户的某个精确到id的评论
        """
        c = Comment.get_instances(self).filter(id=comment_id).filter(user__id=user.id)
        if not c:
            raise BusinessError.ErrNoUserComment
        c.delete()

    def get_comments(self):
        """
        获取某个对象下的comment
        """
        c = Comment.get_instances(self)
        return c

    def get_user_comments(self, user):
        c = Comment.get_instances(self).filter(user__id=user.id)
        return c

    def create_thumbs_up(self, user):
        """点赞，其实就是创建点赞模型的对象

        Args:
            user (_type_): 用户对象

        Raises:
            BusinessError.ErrNoUser: _description_

        Returns:
            ThumbUp: 点赞模型对象
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        tp = ThumbUp.create_instance(self, user=user)
        return tp

    def delete_thumbs_up(self, user):
        """取消点赞

        Args:
            user (_type_): _description_

        Raises:
            BusinessError.ErrNoThumbUp: _description_
        """
        tp = ThumbUp.get_instances(self).filter(
            user__id=user.id).first()  # 如果不存在，则为[]
        if not tp:
            raise BusinessError.ErrNoThumbUp
        tp.delete()

    def get_thumb_up(self, user):
        """获取该对象下的该用户的点赞

        Args:
            user (_type_): _description_

        Returns:
            _type_: _description_
        """
        tp = ThumbUp.get_instances(self).filter(
            user__id=user.id).first()
        return tp

    def get_thumb_ups(self):
        """获取该对象下的所有点赞

        Returns:
            _type_: _description_
        """
        tps = ThumbUp.get_instances(self)
        return tps


class Tag(BaseModel):
    label = models.CharField(max_length=10, verbose_name="标签")
    user = models.ForeignKey(User, verbose_name="创建者",
                             on_delete=models.CASCADE)  # 这个只是记录一下是谁创建的这个tag

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        db_table = "tag"


class Category(BaseModel):
    """
    关于父级分类：
    在创建分类关联的时候，如果选择了二级分类，则需要将一级分类也关联，之后以此类推
    在ser中获取的时候，将实现一颗树
    """
    label = models.CharField(max_length=100, verbose_name="分类")
    parent_category = models.ForeignKey(
        'Category', verbose_name="父级分类", related_name="parent", on_delete=models.CASCADE)
    level = models.IntegerField(default=0, verbose_name="分级")  # 用于记录

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        db_table = "category"
