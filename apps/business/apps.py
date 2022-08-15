from django.apps import AppConfig
from django.db.models.signals import post_migrate


def init_parent_category(sender, *args, **kwargs):
    """初始化父级分类
    先创建父级，再创建其他各级子分类
    """
    need_create = []
    tmp = ["手工", "摄影", "画作", "插花", "潮玩", "数字藏品", "雕塑", "文玩", "雕刻", "其他"]
    from apps.business.models import Category
    cgs = Category.logic_objects.all()
    has_existed = [cg.label for cg in cgs]
    for cate in tmp:
        if cate in has_existed:
            continue
        need_create.append(Category(level=1, label=cate))
    Category.logic_objects.bulk_create(need_create)


def init_all_category(sender, *args, **kwargs):
    categories = {
        "parents": ["手工", "摄影", "画作", "插花", "潮玩", "数字藏品", "雕塑", "文玩", "雕刻", "其他"],
        "手工": [],
        "摄影": [],
        "画作": [],
        "插花": [],
        "潮玩": [],
        "数字藏品": [],
        "雕塑": [],
        "文玩": [],
        "雕刻": [],
        "其他": []
    }


class BusinessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business'
    verbose_name = "通用业务模块"

    def ready(self):
        """
        需要初始化分类数据
        """
        super(BusinessConfig, self).ready()
        post_migrate.connect(init_parent_category, sender=self)
