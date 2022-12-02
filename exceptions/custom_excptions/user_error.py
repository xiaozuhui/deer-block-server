from rest_framework.exceptions import APIException

from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError, Level


class UserError(CustomErrorEnum, APIException):
    # 大概率用在对手机验证码的请求中，手机号已经请求过了，但是还没有超过60秒
    ErrProfileNoExist = CustomError(
        "Profile数据不存在",
        "UF001",
        ErrorType.USER,
        level=Level.ERROR,
    )

    ErrProfileHasExist = CustomError(
        "Profile数据已经存在",
        "UF002",
        ErrorType.USER,
        level=Level.WARN,
    )

    ErrHasFollow = CustomError(
        "您已经关注该用户",
        "UF003",
        ErrorType.USER,
        level=Level.WARN,
    )

    ErrNotFollow = CustomError(
        "您并未关注该用户",
        "UF004",
        ErrorType.USER,
        level=Level.ERROR,
    )
