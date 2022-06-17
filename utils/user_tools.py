import random
import string

from apps.users.models import User
from utils import consts


def get_user_name(phone_number: str = "") -> str:
    """返回系统生成的用户名

    Args:
        phone_number (str, optional): _description_. Defaults to "".

    Returns:
        str: 用户K00013487YD
    """
    first = "".join(random.choices(consts.CHR, k=1)).upper()
    no = User.logic_objects.count() + 1
    mid_no = phone_number[-4:] if phone_number else str(random.random() * 1000)[:4]
    last = "".join(random.choices(consts.CHR, k=2)).upper()
    return "用户 {}".format(first + str(no).rjust(4, '0') + mid_no + last)


def get_user_password(length=12):
    # 随机生成字母和数字的位数
    num_count = random.randint(1, length - 1)
    letter_count = length - num_count
    # 随机抽样生成数字序列
    num_list = [random.choice(string.digits) for _ in range(num_count)]
    # 随机抽样生成字母序列
    letter_list = [random.choice(string.ascii_letters)
                   for _ in range(letter_count)]
    # 合并字母数字序列
    all_list = num_list + letter_list
    # 乱序
    random.shuffle(all_list)
    # 生成目标结果字符串
    result = "".join([i for i in all_list])
    return result
