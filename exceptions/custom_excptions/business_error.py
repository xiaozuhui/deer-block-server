from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError
from rest_framework.exceptions import APIException


class BusinessError(CustomErrorEnum, APIException):
    ErrNoThumbUp = CustomError(
        "不能取消点赞",
        "EI001",
        ErrorType.BUSINESS,
        ""
    ) 

    ErrNoUser = CustomError(
        "用户信息不明",
        "EI002",
        ErrorType.BUSINESS,
        ""
    )

    ErrCanNotThumbup = CustomError(
        "该对象不可点赞",
        "EI003",
        ErrorType.BUSINESS,
        message="这个对象没有继承CanThumbup，所以无法使用对应的方法",
    )
