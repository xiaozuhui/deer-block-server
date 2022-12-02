from rest_framework.exceptions import APIException

from exceptions.custom_errors import CustomErrorEnum, CustomError, ErrorType


class ParamsError(CustomErrorEnum, APIException):
    ErrPostParams = CustomError(
        "POST data 参数错误",
        "EI001",
        ErrorType.PARAMS,
        ""
    )
