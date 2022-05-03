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
