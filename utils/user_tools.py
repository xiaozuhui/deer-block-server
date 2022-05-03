import time
import random

from apps.users.models import User
from utils import consts
from utils.base_tools import random_str_choice
from django.core.cache import cache


def get_user_name(phone_number: str = "") -> str:
    """返回系统生成的用户名

    Args:
        phone_number (str, optional): _description_. Defaults to "".

    Returns:
        str: 用户000013487Y
    """
    no = User.objects.count()+1
    tm = str(time.time()*1000000)[-2:]
    mid_no = phone_number[-2:] if phone_number else str(random.random()*1000)[
        :2]
    last = random_str_choice()
    return "用户{}".format(str(no).rjust(5, '0')+mid_no+tm+last)


def get_register_key(phone_number) -> str:
    """获取注册用户时的缓存key

    Args:
        phone_number (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    if not phone_number:
        raise ValueError("phone number is empty")
    return "register_key_{pn}".format(pn=phone_number)


def get_register_token():
    """获取注册用户时要保存到cache中的token

    """
    code = random.choices(consts.NUM, k=6)
    code = "".join(code)
    return "register_token_{code}".format(code=code), code


def validate_code(phone_number: str, code: str):
    """验证validate code是否正确

    Args:
        phone_number (str): 手机号码
        code (str): 验证码
    """
    if not phone_number:
        raise ValueError("手机号码为空")
    if not code:
        raise ValueError("验证码为空")
    register_key = get_register_key(phone_number)
    saved_code = cache.get(register_key)
    if not saved_code:
        raise ValueError("该手机号已经失效")
    if code == saved_code[-6:]:
        return True
    return False
