from ipaddress import ip_address
from django.db import models
from apps.base_model import BaseModel
from apps.bussiness.models import Category, Tag

from apps.consts import PublishStatus
from apps.interfaces.can_collection import CanCollection
from apps.interfaces.can_share import CanShare
from apps.interfaces.can_thumbup import CanThumbup
from apps.media.models import File
from apps.users.models import User


class Issues(BaseModel, CanShare, CanCollection, CanThumbup):
    """
    动态
    对于一个动态来说，点赞、收藏、回复
    """
    title = models.CharField(max_length=225, verbose_name="动态标题")
    publisher = models.ForeignKey(
        User, verbose_name="发布者", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=PublishStatus.choices, verbose_name="状态", default=PublishStatus.DRAFT)
    content = models.TextField(verbose_name="动态内容")
    medias = models.ManyToManyField(
        File, verbose_name="图片和视频", blank=True)
    # origin存在的意义是，保留之前的修改，标注上一次的版本是什么
    origin = models.ForeignKey(
        'Issues', verbose_name="原动态", related_name="origin_issues",
        blank=True, null=True, on_delete=models.CASCADE)
    # version同理
    version = models.IntegerField(verbose_name="版本", default=0)
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True)
    categories = models.ManyToManyField(
        Category, verbose_name="分类", blank=True)
    # 发布时的ip地址
    ip = models.GenericIPAddressField(
        verbose_name="发布时ip地址", blank=True, null=True)

    class Meta:
        verbose_name = "动态"
        verbose_name_plural = verbose_name
        db_table = "issues"

    def change_status(self, status=None):
        if status == PublishStatus.DRAFT:
            self.status = PublishStatus.DRAFT
        elif status == PublishStatus.PUBLISHED:
            self.status = PublishStatus.PUBLISHED
        else:
            self.status = PublishStatus.ABANDONED
        self.save()


class Reply(BaseModel, CanThumbup):
    """
    动态的回复
    关于动态的回复，每一次回复，都应该提示该回复的“父回复”的“回复者”，以及回复中被@的用户
    并且，必然要提示顶层回复者和动态的发布者
    """
    issues = models.ForeignKey(
        Issues, verbose_name="对应动态", on_delete=models.CASCADE)
    reply = models.ForeignKey('Reply', verbose_name="对应回复", on_delete=models.DO_NOTHING, related_name="re_reply",
                              null=True, blank=True)
    publisher = models.ForeignKey(
        User, verbose_name="回复者", on_delete=models.DO_NOTHING)
    content = models.TextField(verbose_name="回复内容")
    medias = models.ManyToManyField(File, verbose_name="图片和视频")

    class Meta:
        verbose_name = "动态回复"
        verbose_name_plural = verbose_name
        db_table = "replies"

    def __str__(self):
        return "{0}的回复[{1}]".format(self.issues.title, self.publisher.username)
