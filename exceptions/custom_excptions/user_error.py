from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError, Level
from rest_framework.exceptions import APIException


class UserError(CustomErrorEnum, APIException):
    # 大概率用在对手机验证码的请求中，手机号已经请求过了，但是还没有超过60秒
    ErrProfileNoExist = CustomError(
        "Profile数据不存在",
        "UF001",
        ErrorType.USER,
        level=Level.ERROR,
    )
