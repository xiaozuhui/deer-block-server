from rest_framework.exceptions import APIException

from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError


class SendMessageError(CustomErrorEnum, APIException):
    SendFailure = CustomError(
        "发送信息失败",
        "SM001",
        ErrorType.SEND_MEG,
    )

    PhoneNumberEmpty = CustomError(
        "手机号为空",
        "SM002",
        ErrorType.SEND_MEG,
    )

    ValidCodeEmpty = CustomError(
        "验证码为空",
        "SM003",
        ErrorType.SEND_MEG,
    )

    ValidCodeExpire = CustomError(
        "验证码过期，请重新验证",
        "SM004",
        ErrorType.SEND_MEG,
    )

    ValidCodeWrong = CustomError(
        "验证码错误，请重新输入",
        "SM005",
        ErrorType.SEND_MEG,
    )

    UserNotActive = CustomError(
        "用户并非活跃用户，请联系客服",
        "SM006",
        ErrorType.USER,
        message="用户字段is_active为false"
    )

    UserHasDeleted = CustomError(
        "用户已经被删除，请联系客服",
        "SM007",
        ErrorType.USER,
        message="用户字段is_deleted为true"
    )
