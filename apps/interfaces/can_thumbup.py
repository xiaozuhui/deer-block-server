from django.db import models

from apps.bussiness.models import ThumbUp
from exceptions.custom_excptions.business_error import BusinessError


class CanThumbup(models.Model):
    """能够被点赞的模型interface
    """

    def create_thumbsup(self, user):
        """点赞，其实就是创建点赞模型的对象

        Args:
            user (_type_): 用户对象

        Raises:
            BusinessError.ErrNoUser: _description_

        Returns:
            ThumbUp: 点赞模型对象
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        tp = ThumbUp.create_instance(self, tper=user)
        return tp

    def delete_thumbsup(self, user):
        """取消点赞

        Args:
            user (_type_): _description_

        Raises:
            BusinessError.ErrNoThumbUp: _description_
        """
        tp = ThumbUp.get_instances(self).filter(
            tper__id=user.id).first()  # 如果不存在，则为[]
        if not tp:
            raise BusinessError.ErrNoThumbUp
        tp.delete()

    def get_thumbup(self, user):
        """获取该对象下的该用户的点赞

        Args:
            user (_type_): _description_

        Returns:
            _type_: _description_
        """
        tp = ThumbUp.get_instances(self).filter(
            tper__id=user.id).first()
        return tp

    def get_thumbups(self):
        """获取该对象下的所有点赞

        Returns:
            _type_: _description_
        """
        tps = ThumbUp.get_instances(self)
        return tps

    class Meta:
        abstract = True
