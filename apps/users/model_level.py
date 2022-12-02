from django.db import models

from apps.consts import UpgradeUserLevelMethod


class Level(models.Model):
    """
    每一级的称呼是什么
    需要多少经验才能升级
    如何才能涨经验，每次能涨多少经验
    """
    level = models.IntegerField(default=1, verbose_name="阶段等级")
    level_name = models.CharField(verbose_name="等级名称", max_length=255)
    base_upgrade_exp = models.FloatField(verbose_name="基础升级所需经验", default=0.0)
    is_default = models.BooleanField(verbose_name="是否默认等级", default=False)
    next_level = models.ForeignKey('Level', related_name='the_next_level', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "等级"
        verbose_name_plural = verbose_name
        db_table = "level"

    def __str__(self):
        return f"{self.level_name}[{self.level}]"


class LevelGroup(models.Model):
    """
    等级组

    每个UserLevel都会有一个等级组
    接着每个等级组，将会保存一整个有顺序的levelName的列表
    并且还有每升一级的经验
    """
    min_level = models.IntegerField(default=1, verbose_name="最低等级")
    max_level = models.IntegerField(default=99, verbose_name="最高等级")
    upgrade_method = models.ManyToManyField('UpgradeMethod', verbose_name="升级方式")
    levels = models.ManyToManyField(Level, verbose_name="等级")
    is_default = models.BooleanField(verbose_name="是否默认等级组", default=False)

    class Meta:
        verbose_name = "等级组"
        verbose_name_plural = verbose_name
        db_table = "level_group"


class UpgradeMethod(models.Model):
    """
    每个升级的方式
    UserLevel将会从中选择

    可以是点赞升级、评论升级、发表升级
    """
    upgrade_name = models.CharField(max_length=10, choices=UpgradeUserLevelMethod.choices, verbose_name="升级方式")
    # 基础经验值用于锚定每种方式最少的经验值
    base_exp_value = models.FloatField(verbose_name="基础经验值",
                                       help_text="对应的每次达成条件的基础经验值", default=0.0)
    is_default = models.BooleanField(verbose_name="是否默认升级方式", default=False)

    class Meta:
        verbose_name = "升级方式"
        verbose_name_plural = verbose_name
        db_table = "upgrade_method"
