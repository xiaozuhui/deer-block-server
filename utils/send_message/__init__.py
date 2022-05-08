"""该包用于短信、邮箱信息的发送
"""

from deer_block.settings import SEND_MSG_MODE
from utils.send_message.ali_dysms import AliDysms


def dispatch(mod="ral"):
    if SEND_MSG_MODE == 'aliyun':
        return AliDysms(mod)
    return None
