from exceptions.custom_errors import CustomError, ErrorType, CustomErrorEnum


class CodeError(CustomErrorEnum, Exception):
    ErrCodeType = CustomError(
        "错误的编码类型",
        "EC001",
        ErrorType.CODE,
        "编码类型应该为以下种类：",
    )

    ErrCodeIsNull = CustomError(
        "编码为空",
        "EC002",
        ErrorType.CODE,
        "编码最终没有生成或是缺失"
    )
