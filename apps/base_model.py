import datetime
from typing import List
from django.db import models
from apps import custom_manager


class BaseModel(custom_manager.LogicDeleteModel):
    """
    基础模型，继承django的模型和逻辑删除主模型
    """
    created_at = models.DateTimeField(
        verbose_name="数据创建时间", auto_now=True, null=True)
    updated_at = models.DateTimeField(
        verbose_name="数据更新时间", auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(
        verbose_name="数据失效时间", null=True, blank=True)

    class Meta:
        abstract = True

    @staticmethod
    def compare(request_data, model_intance, compare_items: List[str]):
        """对比request.Data和对应的model_data之间的数据比较
        """
        for compare_item in compare_items:
            item = request_data.get(compare_item, None)
            if not hasattr(model_intance, compare_item):
                return False
            model_item = getattr(model_intance, compare_item)
            if item != model_item:
                return False
        return True
