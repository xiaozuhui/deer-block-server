from apps.base_model import BaseModel
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from django.db import models

from apps.consts import UserGender
from apps.custom_models import ImageField

logger = logging.getLogger(__name__)


class UserProfile(BaseModel):
    """
    用户概述
    """
    user = models.OneToOneField(User,
                                verbose_name="用户",
                                db_constraint=False,
                                on_delete=models.CASCADE,
                                related_name="profile_user")
    gender = models.CharField(max_length=20,
                              verbose_name="性别",
                              choices=UserGender.choices,
                              blank=True)
    avatar = ImageField(verbose_name='用户头像',
                        null=True,
                        blank=True,
                        related_name="user_avatar")
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    city = models.CharField(max_length=50, blank=True,
                            null=True, verbose_name="城市")
    address = models.CharField(
        max_length=215, blank=True, null=True, verbose_name="地址")
    signature = models.CharField(
        max_length=215, verbose_name="签名", blank=True, null=True)

    # 关注与被关注
    follow = models.ManyToManyField(
        User, related_name="user_follow", verbose_name='关注', blank=True)
    followed = models.ManyToManyField(
        User, related_name="user_followed", verbose_name='被关注', blank=True)
    
    ip = models.GenericIPAddressField(
        verbose_name="注册时ip地址", blank=True, null=True)

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name
        db_table = "user_profile"

    def __str__(self):
        return self.user.username

    @property
    def phone_number(self):
        return self.user.phone_number

    @property
    def current_user_id(self):
        return self.user.id

    @property
    def username(self):
        return self.user.username


@receiver(post_save, sender=User, dispatch_uid="user_post_save")
def user_create_handler(sender, instance, **kwargs):
    logger.info("创建User[{}]的UserProfile信息".format(instance))
    profiles = UserProfile.logic_objects.filter(user__id=instance.id)
    if profiles:
        return
    profile = UserProfile()
    profile.user = instance
    profile.save()


class UserPayment(BaseModel):
    """绑定支付宝、绑定微信、实名认证
    """
    user = models.OneToOneField(User,
                                verbose_name="用户",
                                db_constraint=False,
                                on_delete=models.CASCADE,
                                related_name="payment_user")

    class Meta:
        verbose_name = "支付功能"
        verbose_name_plural = verbose_name
        db_table = "user_payment"
