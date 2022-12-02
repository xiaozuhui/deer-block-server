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


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


def to_human_size(size):
    """将bit大小转换为可读的大小

    Args:
        size (_type_): _description_

    Returns:
        _type_: _description_
    """
    fs = "0 MB"
    if size > 1024 * 1024:
        fs = "{:.2f} MB".format(size / (1024 * 1024))
    elif size > 1024:
        fs = "{:.2f} KB".format(size / 1024)
    else:
        fs = "{:.2f} B".format(size)
    return fs
