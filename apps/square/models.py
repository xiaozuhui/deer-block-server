from django.db import models

from apps.base_model import BaseModel
from apps.bussiness.models import Category, Tag, Comment, ThumbUp
from apps.consts import PublishStatus
from apps.custom_models import ImageField
from apps.interfaces.can_collection import CanCollection
from apps.interfaces.can_comment import CanComment
from apps.interfaces.can_share import CanShare
from apps.interfaces.can_thumbup import CanThumbUp
from apps.media.models import File
from apps.users.models import User
from exceptions.custom_excptions.business_error import BusinessError


class Issues(BaseModel, CanShare, CanCollection, CanThumbUp, CanComment):
    """
    动态
    对于一个动态来说，点赞、收藏、回复
    """
    title = models.CharField(max_length=225, verbose_name="动态标题")
    publisher = models.ForeignKey(User, verbose_name="发布者", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PublishStatus.choices, verbose_name="状态",
                              default=PublishStatus.DRAFT)
    content = models.TextField(verbose_name="动态内容")
    medias = models.ManyToManyField(File, verbose_name="图片和视频", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True)
    categories = models.ManyToManyField(Category, verbose_name="分类", blank=True)
    # 发布时的ip地址
    ip = models.GenericIPAddressField(verbose_name="发布时ip地址", blank=True, null=True)
    # 标识这个issues是不是纯粹的视频动态
    is_video_issues = models.BooleanField(verbose_name="是否是视频动态", default=False)
    # 视频封面
    video_image = ImageField(verbose_name='视频封面',
                             null=True,
                             blank=True,
                             related_name="video_image")

    class Meta:
        verbose_name = "动态"
        verbose_name_plural = verbose_name
        db_table = "issues"

    # 实现接口
    def create_comment(self, user, content, medias=None, ip=None, *args, **kwargs):
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
        if not content and not medias:
            # 如果既没有内容又没有图片，则报错
            raise BusinessError.ErrContentEmpty
        if not medias:
            comment = Comment.create_instance(self, user=user, content=content, ip=ip)
        else:
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
