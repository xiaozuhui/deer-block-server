import random

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.base_model import BaseModel
from utils import consts


def default_user_code():
    first = "".join(random.choices(consts.CHR, k=1)).upper()
    no = 9999
    mid_no = str(random.random() * 1000)[:4]
    last = "".join(random.choices(consts.CHR, k=2)).upper()
    user_code = first + str(no).rjust(4, '0') + mid_no + last
    return user_code


class User(AbstractUser, BaseModel):
    """
    自定义用户信息, 使用基本user, 加入手机号即可
    """
    phone_number = models.CharField(max_length=14, verbose_name="手机号", unique=True)
    user_code = models.CharField(max_length=20, verbose_name="用户编码", unique=True, default=default_user_code)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']
