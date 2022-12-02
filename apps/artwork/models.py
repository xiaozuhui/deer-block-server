from django.db import models

from apps.base_model import BaseModel
from apps.business.models import Category, Tag
from apps.interfaces.can_collection import CanCollection
from apps.interfaces.can_share import CanShare
from apps.media.models import File
from apps.users.models import User


class Art(BaseModel, CanShare, CanCollection):
    """
    艺术品 可以分享，可以收藏
        - 标题
        - 创作时间
        - 作者
        - 是否原创
        - 作者基本信息
        - 上传者
        - 是否上传者拥有
        原创意味着拥有

    艺术品和商品是一对一的，艺术品转为商品，就是创建为商品，或是商品的上架
    """
    title = models.CharField(verbose_name="艺术品标题", max_length=255, default="无题")
    author = models.ForeignKey("Author", verbose_name="作家", on_delete=models.DO_NOTHING)
    creative_work_time = models.CharField(max_length=20, verbose_name="创作时间", null=True, blank=True)
    is_original = models.BooleanField(verbose_name="是否原创", default=True)
    uploader = models.ForeignKey(User, verbose_name="上传者", on_delete=models.CASCADE, related_name="art_uploader")
    is_uploader_has = models.BooleanField(verbose_name="是否上传者拥有", default=True)
    medias = models.ManyToManyField(File, verbose_name="图片或视频", blank=True)

    category = models.ManyToManyField(Category, verbose_name="分类")
    tags = models.ManyToManyField(Tag, verbose_name="标签")

    last_width = models.FloatField(verbose_name="最宽处宽度", default=0, help_text="单位厘米(cm)")
    last_length = models.FloatField(verbose_name="最长处长度", default=0, help_text="单位厘米(cm)")
    last_height = models.FloatField(verbose_name="最高处高度", default=0, help_text="单位厘米(cm)")

    class Meta:
        verbose_name = "艺术品"
        verbose_name_plural = verbose_name
        db_table = "art"


class Author(BaseModel, CanCollection):
    """
    作者信息，可以为User本身，也可以是写入信息
    """
    name = models.CharField(verbose_name="作者姓名", max_length=255, default="佚名")
    birthday = models.CharField(verbose_name="出身年月", max_length=50, null=True, blank=True)
    introduce = models.TextField(verbose_name="介绍", default="")
    address = models.CharField(verbose_name="联系地址", max_length=512, null=True, blank=True)
    contact = models.CharField(verbose_name="联系方式", max_length=50, null=True, blank=True, help_text="联系电话或手机号码")
    # 如果是原创，可以直接关联到作家
    related_user = models.ForeignKey(User, verbose_name="关联用户", null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "作者信息"
        verbose_name_plural = verbose_name
        db_table = "author"
