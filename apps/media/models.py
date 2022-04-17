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
    uploader_id = models.IntegerField(
        verbose_name="上传者id", blank=True, null=True)
    uploader_name = models.CharField(
        max_length=50, verbose_name="上传者姓名", blank=True, null=True)
    sequence = models.IntegerField(verbose_name="顺序", default=0)
    upload_time = models.DateTimeField(
        verbose_name="上传时间", auto_now=True)  # 上传时间
    is_active = models.BooleanField(verbose_name="是否有效", default=True)
    is_private = models.BooleanField(verbose_name="是否私有", default=False)

    class Meta:
        verbose_name = "基础文件管理"
        verbose_name_plural = verbose_name

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
        return self.file.size
