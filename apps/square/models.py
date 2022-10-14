from django.db import models

from apps.base_model import BaseModel
from apps.business.models import Category, Tag, Comment, ThumbUp
from apps.consts import PublishStatus
from apps.custom_models import ImageField
from apps.interfaces.can_collection import CanCollection
from apps.interfaces.can_comment import CanComment
from apps.interfaces.can_share import CanShare
from apps.interfaces.can_thumbup import CanThumbUp
from apps.media.models import File
from apps.users.models import User


class Issues(BaseModel, CanShare, CanCollection, CanThumbUp, CanComment):
    """
    动态
    对于一个动态来说，点赞、收藏、回复
    """
    title = models.CharField(max_length=225, verbose_name="动态标题", null=True, blank=True)
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
