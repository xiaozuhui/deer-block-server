from uuid import uuid4
from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.consts import FileType
from apps.users.models import User
import utils.base_tools as tools


def default_array():
    return []


class File(models.Model):
    """文件类型
    统一存于minio中
    """
    file_list = ArrayField(models.UUIDField(), size=9, default=default_array)
    uploader = models.ForeignKey(User, verbose_name="上传者", blank=True, null=True, related_name="uploader",
                                 on_delete=models.CASCADE)
    upload_time = models.DateTimeField(
        verbose_name="上传时间", auto_now=True)  # 上传时间
    remarks = models.TextField(verbose_name="备注", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="是否有效", default=True)

    class Meta:
        verbose_name = "基础文件管理"
        verbose_name_plural = verbose_name
        db_table = "file"

    @property
    def file_size(self):
        """
        获取文件的大小
        """
        files = FileStorage.objects.filter(uuid__in=self.file_list)
        amount = 0
        for f in files:
            amount += f.f_size()
        fs = tools.to_human_size(amount)
        return fs


class FileStorage(models.Model):
    """为了实现多文件上传，每一次上传都是用arrayfield来存储文件对应的uuid
    """
    filename = models.CharField(max_length=225, verbose_name="文件名", default="")
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)  # 主键
    file = models.FileField(verbose_name="文件", upload_to="")
    sequence = models.IntegerField(verbose_name="顺序", default=0)
    is_private = models.BooleanField(verbose_name="是否私有", default=False)
    # 文件类型相关字段
    file_type = models.CharField(max_length=20,
                                 verbose_name="文件类型",
                                 choices=FileType.choices,
                                 default=FileType.NONE)
    file_extension = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="文件后缀")
    mime_type = models.CharField(
        max_length=215, blank=True, null=True, verbose_name="内部类型")

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.file.name
        super(FileStorage, self).save(*args, **kwargs)

    @property
    def file_url(self):
        """
        获取文件url
        """
        return self.file.url

    @property
    def file_name(self):
        """
        获取上传文件本身的名字
        """
        return self.file.name

    @property
    def file_size(self):
        """
        获取文件的大小
        """
        fs = self.file.size
        return tools.to_human_size(fs)

    def f_size(self):
        return self.file.size

    @classmethod
    def pares_file_type(cls, m_type):
        if m_type == "video":
            return FileType.VIDEO
        elif m_type == "audio":
            return FileType.AUDIO
        elif m_type == "image":
            return FileType.IMAGE
        else:
            return FileType.OTHER
