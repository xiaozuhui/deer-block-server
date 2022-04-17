from django.db import models

from apps.media.models import File


class ImageField(models.ForeignKey):
    """
    ImageField
    圖片类型字段
    """

    def __init__(self, to=File, **kwargs):
        """图片类型的自定义模型
        是一个外健类型
        """
        related_name = kwargs.get("related_name", None)
        if not related_name:
            raise Exception("related_name 字段不能为空")
        related_query_name = kwargs.get("related_query_name", None)
        parent_link = kwargs.get("parent_link", False)
        db_constraint = kwargs.get("db_constraint", True)
        limit_choices_to = kwargs.get("limit_choices_to", None)
        to_field = kwargs.get("to_field", None)
        super().__init__(to=to, related_query_name=related_query_name, limit_choices_to=limit_choices_to,
                         parent_link=parent_link, to_field=to_field, db_constraint=db_constraint,
                         on_delete=models.DO_NOTHING, related_name=related_name, null=True, blank=True)
