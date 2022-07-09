from rest_framework.exceptions import APIException

from exceptions.custom_errors import CustomErrorEnum, ErrorType, CustomError, Level


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

    ErrContentEmpty = CustomError(
        "评论内容不能为空",
        "EI004",
        ErrorType.BUSINESS,
        ""
    )

    ErrCanNotThumbup = CustomError(
        "该对象不可点赞",
        "EI003",
        ErrorType.BUSINESS,
        message="这个对象没有实现可以点赞的接口，所以无法使用对应的方法",
    )

    ErrNoComment = CustomError(
        "没有相关评论",
        "EI005",
        ErrorType.BUSINESS,
    )

    ErrNoCollection = CustomError(
        "没有收藏，无法删除",
        "EI006",
        ErrorType.BUSINESS,
    )

    ErrNoCommentId = CustomError(
        "没有评论id",
        "EI007",
        ErrorType.BUSINESS,
    )

    ErrNoUserComment = CustomError(
        "该用户没有评论或是该用户的评论与所传id不符",
        "EI008",
        ErrorType.BUSINESS,
        level=Level.WARN
    )

    ErrErrorMethod = CustomError(
        "错误的请求",
        "EI009",
        ErrorType.BUSINESS,
        level=Level.ERROR
    )
