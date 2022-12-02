from apps.business.models import Collection
from exceptions.custom_excptions.business_error import BusinessError


class CanCollection:
    """能够被收藏的模型interface
    """

    def create_collect(self, user):
        """
        创建收藏
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        c = Collection.create_instance(self, user=user)
        return c

    def delete_collect(self, user):
        """
        取消收藏
        """
        c = Collection.get_instances(self).filter(user__id=user.id).first()  # 如果不存在，则为[]
        if not c:
            raise BusinessError.ErrNoCollection
        c.delete()

    def get_collect(self, user):
        """获取该对象下该用户的收藏对象
        """
        c = Collection.get_instances(self).filter(user__id=user.id).first()
        return c

    def get_collects(self):
        """
        获取该对象下所有的收藏对象
        """
        c = Collection.get_instances(self)
        return c
