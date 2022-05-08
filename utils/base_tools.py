import random

from utils import consts


def random_str_choice(n: int = 1, is_upper: bool = True) -> str:
    """获取n位的随机字符

    Args:
        n (int, optional): _description_. Defaults to 1.
        is_upper (bool, optional): _description_. Defaults to True.

    Returns:
        str: _description_
    """
    res = str(random.choices(consts.CHR, k=n))
    return res.upper() if is_upper else res


def singleton(cls, *args, **kwargs):
    """单例装饰器

    Returns:
        _type_: _description_
    """
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton
