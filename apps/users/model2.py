import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.base_model import BaseModel
from apps.consts import UserGender, PaymentType
from apps.custom_models import ImageField
from apps.users.model_level import LevelGroup
from .models import User

logger = logging.getLogger('django')


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
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="城市")
    address = models.CharField(max_length=215, blank=True, null=True, verbose_name="地址")
    autograph = models.CharField(max_length=215, verbose_name="签名", blank=True, null=True)

    # 关注
    follow = models.ManyToManyField(User, related_name="user_follow", verbose_name='关注', blank=True)
    ip = models.GenericIPAddressField(verbose_name="注册时ip地址", blank=True, null=True)

    # 用户等级
    user_level = models.IntegerField(verbose_name="用户等级", default=0)
    has_exp = models.FloatField(verbose_name="以获取经验", default=0.0)  # 升级之后要不要归零？
    level_group = models.ForeignKey(LevelGroup, on_delete=models.DO_NOTHING,
                                    verbose_name="等级组", null=True)

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
    lg = LevelGroup.objects.filter(is_default=True).first()
    if lg:
        profile.level_group = lg
    else:
        logger.error("默认的level_group不存在")
    profile.save()


class RealNameAuth(BaseModel):
    """
    实名认证
    保存基本信息后，将会请求认证接口，然后将会写回is_active
    后续判断都将围绕is_active
    """
    user = models.OneToOneField(User,
                                verbose_name="用户",
                                db_constraint=False,
                                on_delete=models.CASCADE,
                                related_name="real_user")
    real_name = models.CharField(max_length=10, verbose_name="真实姓名")
    id_number = models.CharField(max_length=20, verbose_name="身份证号", unique=True)
    is_active = models.BooleanField(verbose_name="是否已经验证", default=False)


class UserPayment(BaseModel):
    """暂时
        绑定支付宝
        绑定微信
        绑定银联
        常用支付方式
    """
    user = models.OneToOneField(User,
                                verbose_name="用户",
                                db_constraint=False,
                                on_delete=models.CASCADE,
                                related_name="payment_user")
    constant_way = models.CharField(choices=PaymentType.choices, verbose_name="常用支付方式",
                                    max_length=20, default=PaymentType.WEIXIN)

    class Meta:
        verbose_name = "支付功能"
        verbose_name_plural = verbose_name
        db_table = "user_payment"
