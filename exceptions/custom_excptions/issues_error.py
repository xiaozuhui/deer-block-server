from rest_framework.exceptions import APIException

from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError


class IssuesError(CustomErrorEnum, APIException):
    ErrNoneTitle = CustomError(
        "动态没有标题",
        "EI001",
        ErrorType.ISSUES,
        ""
    )

    ErrNotExist = CustomError(
        "找不到动态数据",
        "EI002",
        ErrorType.ISSUES,
        ""
    )

    ErrParamNoId = CustomError(
        "参数缺少id",
        "EI003",
        ErrorType.ISSUES,
        ""
    )

    ErrAbandonInstance = CustomError(
        "该动态已经废弃，不能修改或更新",
        "EI004",
        ErrorType.ISSUES,
        ""
    )

    ErrHasPublished = CustomError(
        "该动态已经发布，无法发布",
        "EI005",
        ErrorType.ISSUES,
        ""
    )
