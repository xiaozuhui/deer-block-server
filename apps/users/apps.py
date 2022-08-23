import logging

from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_migrate

from apps.consts import UpgradeUserLevelMethod

logger = logging.getLogger(__name__)


def _init_superuser(sender, *args, **kwargs):
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
        "user_code": "system001",
        "is_superuser": True,
        "is_staff": True,
        "is_active": True,
    }
    User.logic_objects.create(**user_info)
    logger.info("创建超级用户neo")


def _init_level(sender, *args, **kwargs):
    """
    初始化默认等级和等级组、升级方式
    """
    # 升级方式
    from apps.users.model_level import UpgradeMethod, Level, LevelGroup
    methods = []
    ums = UpgradeMethod.objects.filter(is_default=True)
    has_existed = [u.upgrade_name for u in ums]
    for lm in UpgradeUserLevelMethod.choices:
        if lm[0] in has_existed:
            continue
        um = UpgradeMethod(upgrade_name=lm[0], base_exp_value=5, is_default=True)
        methods.append(um)
    if methods:
        methods = UpgradeMethod.objects.bulk_create(methods)
    else:
        logger.info("没有需要创建的默认升级方式")

    # 等级Level
    levels = []
    ls = Level.objects.filter(is_default=True)
    has_existed = [u.level_name for u in ls]
    for i in range(1, 6):
        if f"等级{i}" in has_existed:
            continue
        levels.append(Level(
            level=i,
            level_name=f"等级{i}",
            base_upgrade_exp=i * 100 - (25 * i if i > 10 else 15 * i - 10),
            is_default=True,
        ))

    if levels:
        levels = Level.objects.bulk_create(levels)
        last = None
        for level in levels[::-1]:
            # 倒序创建外键
            if level == levels[-1]:
                last = level
                continue
            if level is None:
                continue
            level.next_level = last
            level.save()
            last = level
    else:
        logger.info("没有需要创建的默认等级")

    # 等级组
    lg = LevelGroup.objects.filter(is_default=True).first()
    if lg:
        methods = UpgradeMethod.objects.filter(is_default=True)
        levels = Level.objects.filter(is_default=True)
        lg.upgrade_method.set(methods)
        lg.levels.set(levels)
        lg.save()
    else:
        lg = LevelGroup()
        lg.min_level = 1
        lg.max_level = 6
        lg.is_default = True
        lg.save()
        lg.upgrade_method.add(*methods)
        lg.levels.add(*levels)
        lg.save()


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = "用户信息模块"

    def ready(self):
        super(UserConfig, self).ready()
        post_migrate.connect(_init_level, sender=self)
        post_migrate.connect(_init_superuser, sender=self)
