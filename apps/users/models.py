from django.contrib.auth import get_user_model
from django.db import models

from apps.consts import UserGender
from apps.media.models import File
from apps.custom_models import ImageField


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name="用户", db_constraint=False, on_delete=models.CASCADE,
                                related_name="profile")
    nick_name = models.CharField(max_length=120, default='', verbose_name='昵称')
    phone = models.CharField(max_length=20, verbose_name="手机号", unique=True)
    sex = models.CharField(max_length=20, verbose_name="性别",
                           choices=UserGender.choices, blank=True)
    avatar = ImageField(File, verbose_name='用户头像', null=True, blank=True, related_name="user_avatar")
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    # TODO 绑定支付宝、绑定微信、实名认证

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.phone) + '  ' + str(self.user.id)
