import logging

from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_migrate

logger = logging.getLogger(__name__)


def init_superuser(sender, *args, **kwargs):
    """需要初始化superuser数据（或是管理员数据）
    superuser: neo - 1qazXDR%!admin
    """
    from apps.users.models import User
    if User.logic_objects.filter(is_superuser=True).count() != 0:
        logger.error("不需要初始化创建超级用户，已经存在超级用户")
        return
    user_info = {
        'username': "neo",
        "phone_number": "00000000000",
        "password": make_password("1qazXDR%!admin"),
        "is_superuser": True,
        "is_staff": True,
        "is_active": True,
    }
    User.logic_objects.create(**user_info)
    logger.info("创建超级用户neo")


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = "用户信息模块"

    def ready(self):
        super(UserConfig, self).ready()
        post_migrate.connect(init_superuser, sender=self)
