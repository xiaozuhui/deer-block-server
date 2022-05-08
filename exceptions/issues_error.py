from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError


class IssuesError(CustomErrorEnum, Exception):
    ErrNoneTitle = CustomError(
        "动态没有标题",
        "EI001",
        ErrorType.ISSUES,
        ""
    )
