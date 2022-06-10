from django.db import models

from apps.bussiness.models import Collection
from exceptions.custom_excptions.business_error import BusinessError


class CanCollection(models.Model):
    """能够被收藏的模型interface
    """

    class Meta:
        abstract = True

    def create_collect(self, user):
        """
        创建收藏
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        c = Collection.create_instance(self, collecter=user)
        return c

    def delete_collect(self, user):
        """
        取消收藏
        """
        tp = Collection.get_instances(self).filter(
            collecter__id=user.id).first()  # 如果不存在，则为[]
        if not tp:
            raise BusinessError.ErrNoThumbUp
        tp.delete()

    def get_collect(self, user):
        """获取该对象下该用户的收藏对象
        """
        tp = Collection.get_instances(self).filter(
            collecter__id=user.id).first()
        return tp

    def get_collects(self):
        """
        获取该对象下所有的收藏对象
        """
        tps = Collection.get_instances(self)
        return tps
