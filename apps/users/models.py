from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.base_model import BaseModel


class User(AbstractUser, BaseModel):
    """
    自定义用户信息, 使用基本user, 加入手机号即可
    """
    phone_number = models.CharField(
        max_length=14, verbose_name="手机号", unique=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']
