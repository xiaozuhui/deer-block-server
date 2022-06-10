from django.db import models

from apps.bussiness.models import Share
from exceptions.custom_excptions.business_error import BusinessError


class CanShare(models.Model):
    """能够被分享的模型interface
    """
    class Meta:
        abstract = True

    def create_share(self, user, share_url="", share_type=""):
        """创建一条分享链接

        Args:
            user (User): 登录用户
            share_url (str, optional): 生成的分享链接. Defaults to "".
            share_type (str, optional): 分享的类型. Defaults to "".

        Raises:
            BusinessError.ErrNoUser: 没有用户异常

        Returns:
            _type_: _description_
        """
        if not user:
            raise BusinessError.ErrNoUser
        share = Share.create_instance(
            self, sharer=user, share_url=share_url, share_type=share_type)
        return share

    def get_all_share(self):
        """获取该项目下的所有分享数据

        Returns:
            Share: _description_
        """
        shares = Share.get_instances(self)
        return shares

    def get_shares(self, user):
        """获取该项目下、该用户做出的分享数据

        Args:
            user (User): 登录用户

        Returns:
            _type_: _description_
        """
        shares = Share.get_instances(self).filter(sharer__id=user.id)
        return shares
