import string
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
        str: 用户K00013487YD
    """
    first = "".join(random.choices(consts.CHR, k=1)).upper()
    no = User.logic_objects.count()+1
    mid_no = phone_number[-4:] if phone_number else str(random.random()*1000)[:4]
    last = "".join(random.choices(consts.CHR, k=2)).upper()
    return "用户 {}".format(first+str(no).rjust(4, '0')+mid_no+last)


def get_user_password(length=12):
    # 随机生成字母和数字的位数
    numcount = random.randint(1, length-1)
    lettercount = length - numcount
    # 随机抽样生成数字序列
    numlist = [random.choice(string.digits) for _ in range(numcount)]
    # 随机抽样生成字母序列
    letterlist = [random.choice(string.ascii_letters)
                  for _ in range(lettercount)]
    # 合并字母数字序列
    alllist = numlist + letterlist
    # 乱序
    result = random.shuffle(alllist)
    # 生成目标结果字符串
    result = "".join([i for i in alllist])
    return result
