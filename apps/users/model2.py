from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from django.contrib.auth import get_user_model
from django.db import models

from apps.consts import UserGender
from apps.custom_models import ImageField

logger = logging.getLogger(__name__)


class UserProfile(models.Model):
    """
    用户概述
    """
    user = models.OneToOneField(get_user_model(),
                                verbose_name="用户",
                                db_constraint=False,
                                on_delete=models.CASCADE,
                                related_name="profile")
    gender = models.CharField(max_length=20,
                              verbose_name="性别",
                              choices=UserGender.choices,
                              blank=True)
    avatar = ImageField(verbose_name='用户头像',
                        null=True,
                        blank=True,
                        related_name="user_avatar")
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')

    # TODO 绑定支付宝、绑定微信、实名认证

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name
        db_table = "user_profile"

    def __str__(self):
        return self.user.username

    @property
    def phone_number(self):
        return self.user.phone_number


@receiver(post_save, sender=User, dispatch_uid="user_post_save")
def user_create_handler(sender, instance, **kwargs):
    logger.info("创建User[{}]的UserProfile信息".format(instance))
    profiles = UserProfile.objects.filter(user__id=instance.id)
    if profiles:
        return
    profile = UserProfile()
    profile.user = instance
    profile.save()
