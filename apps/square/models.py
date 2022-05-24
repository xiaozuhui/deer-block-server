from django.db import models
from apps.base_model import BaseModel

from apps.consts import PublishStatus
from apps.media.models import File
from apps.users.models import User


class Issues(BaseModel):
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
    medias = models.ManyToManyField(File, verbose_name="图片和视频")
    # origin存在的意义是，保留之前的修改，标注上一次的版本是什么
    origin = models.ForeignKey(
        'Issues', verbose_name="原动态", related_name="origin_issues", null=True, on_delete=models.CASCADE)
    # version同理
    version = models.IntegerField(verbose_name="版本", default=0)

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


class Collection(models.Model):
    """
    收藏，收藏不需要使用逻辑删除
    收藏只能对应动态来收藏，而不能收藏回复
    """
    publisher = models.ForeignKey(
        User, verbose_name="收藏者", on_delete=models.CASCADE)
    issues = models.ForeignKey(
        Issues, verbose_name="对应动态", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name
        db_table = "collection"


class ThumbsUp(models.Model):
    """
    点赞，点赞不需要逻辑删除
    但是点赞可以对回复进行点赞
    """
    publisher = models.ForeignKey(
        User, verbose_name="点赞者", on_delete=models.CASCADE)
    issues = models.ForeignKey(
        Issues, verbose_name="对应动态", on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(
        'Reply', verbose_name="对应回复", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
        db_table = "thumbs_up"


class Share(models.Model):
    publisher = models.ForeignKey(
        User, verbose_name="分享者", on_delete=models.CASCADE)
    issues = models.ForeignKey(
        Issues, verbose_name="对应动态", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = verbose_name
        db_table = "share"


class Reply(BaseModel):
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
