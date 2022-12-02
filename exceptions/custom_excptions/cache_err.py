from rest_framework.exceptions import APIException

from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError, Level


class CacheRequestError(CustomErrorEnum, APIException):
    # 大概率用在对手机验证码的请求中，手机号已经请求过了，但是还没有超过60秒
    ExistToken = CustomError(
        "请求已经存在并且还未失效",
        "CR001",
        ErrorType.CACHE,
        level=Level.WARN,
    )
