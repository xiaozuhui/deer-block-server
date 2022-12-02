import random
import string


def get_level_code():
    """
    生成LevelMethod的编码
    LM-8635-IU
    """
    prefix = "LM"
    num_list = [random.choice(string.digits) for _ in range(4)]
    # 乱序
    random.shuffle(num_list)
    # 生成目标结果字符串
    nums = "".join([i for i in num_list])
    letter_list = [random.choice(string.ascii_letters) for _ in range(2)]
    return prefix + "".join([i for i in nums]) + "".join([i for i in letter_list]).upper()
