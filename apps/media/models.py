from django.contrib.auth.models import User
from django.db import models
from apps.consts import FileType


class File(models.Model):
    """文件类型
    统一存于SSO中
    """
    title = models.CharField(
        max_length=120, verbose_name="文件标题", blank=True, null=True)
    file_type = models.CharField(
        max_length=50, verbose_name="文件类型", choices=FileType.choices, default=FileType.NONE)
    file = models.FileField(verbose_name="文件", upload_to="")
    uploader = models.ForeignKey(User, verbose_name="上传者", blank=True, null=True, related_name="uploader",
                                 on_delete=models.CASCADE)
    sequence = models.IntegerField(verbose_name="顺序", default=0)
    upload_time = models.DateTimeField(
        verbose_name="上传时间", auto_now=True)  # 上传时间
    remarks = models.TextField(verbose_name="备注", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="是否有效", default=True)
    is_private = models.BooleanField(verbose_name="是否私有", default=False)
    # hash_code = models.CharField(max_length=32, verbose_name="哈希值", default="")

    class Meta:
        verbose_name = "基础文件管理"
        verbose_name_plural = verbose_name
        db_table = "file"

    def __str__(self):
        return self.title if self.title else self.file_name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.file.name
        super(File, self).save(*args, **kwargs)

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
        file_size = self.file.size
        fs = "0 MB"
        if file_size > 1024 * 1024:
            fs = "{:.2f} MB".format(file_size / (1024 * 1024))
        elif file_size > 1024:
            fs = "{:.2f} KB".format(file_size / 1024)
        else:
            fs = "{:.2f} B".format(file_size)
        return fs
