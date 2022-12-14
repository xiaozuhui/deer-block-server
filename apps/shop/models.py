from django.db import models

from apps.artwork.models import Art
from apps.base_model import BaseModel
from apps.business.models import Tag
from apps.interfaces.can_collection import CanCollection
from apps.interfaces.can_comment import CanComment
from apps.interfaces.can_share import CanShare
from apps.interfaces.can_thumbup import CanThumbUp


class Product(BaseModel, CanShare, CanCollection, CanThumbUp, CanComment):
    """
    商品，必须关联到Art模型
    可以分享、可以收藏、可以点赞、可以评论
    """
    art = models.OneToOneField(Art, verbose_name="艺术品", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="价格", max_digits=32, decimal_places=4)
    tags = models.ManyToManyField(Tag, verbose_name="标签")
    is_grounding = models.BooleanField(verbose_name="是否上架", default=False)
    count = models.IntegerField(verbose_name="数量", default=1)  # 可能手工品，可以做多个
