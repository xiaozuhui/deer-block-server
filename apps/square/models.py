from django.contrib.auth.models import User
from django.db import models

from apps.consts import PublishStatus
from apps.media.models import File


class Issues(models.Model):
    """
    动态
    对于一个动态来说，点赞、收藏、回复，是三个主要附属品
    如果动态是任务动态，那么是不是应该分开来操作？
    """
    title = models.CharField(max_length=225, verbose_name="动态标题")
    publisher = models.ForeignKey(User, verbose_name="发布者", on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=PublishStatus.choices, verbose_name="状态")
    content = models.TextField(verbose_name="动态内容")
    medias = models.ManyToManyField(File, verbose_name="图片和视频")

    class Meta:
        verbose_name = "动态"
        verbose_name_plural = verbose_name
        db_table = "issues"


class Collection(models.Model):
    """
    收藏
    """
    who = models.ForeignKey(User, verbose_name="收藏者", on_delete=models.CASCADE)
    issues = models.ForeignKey(Issues, verbose_name="对应动态", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name
        db_table = "collection"

    def __str__(self):
        return "{0} - {1}".format(str(self.issues), self.who.username)


class ThumbsUp(models.Model):
    """
    点赞
    """
    who = models.ForeignKey(User, verbose_name="点赞者", on_delete=models.CASCADE)
    dy_info = models.ForeignKey(Issues, verbose_name="对应动态", on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey('Reply', verbose_name="对应回复", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
        db_table = "thumbs_up"


class Reply(models.Model):
    """
    动态的回复
    关于动态的回复，每一次回复，都应该提示该回复的“父回复”的“回复者”，以及回复中被@的用户
    并且，必然要提示顶层回复者和动态的发布者
    """
    issues = models.ForeignKey(Issues, verbose_name="对应动态", on_delete=models.CASCADE)
    reply = models.ForeignKey('Reply', verbose_name="对应回复", on_delete=models.DO_NOTHING, related_name="re_reply",
                              null=True, blank=True)
    replier = models.ForeignKey(User, verbose_name="回复者", on_delete=models.DO_NOTHING)
    content = models.TextField(verbose_name="回复内容")
    medias = models.ManyToManyField(File, verbose_name="图片和视频")

    class Meta:
        verbose_name = "动态回复"
        verbose_name_plural = verbose_name
        db_table = "replies"

    def __str__(self):
        return "{0}的回复[{1}]".format(self.issues.title, self.replier.username)
