from rest_framework.exceptions import APIException

from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError


class LevelError(CustomErrorEnum, APIException):
    ErrWrongOperator = CustomError(
        "错误的升级操作",
        "LE001",
        ErrorType.LEVEL,
        ""
    )

    ErrWrongUserLevel = CustomError(
        "员工的level存在错误",
        "LE002",
        ErrorType.LEVEL,
        ""
    )
