from enum import Enum

from rest_framework.exceptions import APIException


class ErrorType(Enum):
    """
    这个枚举是用来提供错误类型的
    例：
    code = 是用来标识生成编码或是跟编码有关的错误
    shop = 是用来标识商店相关的错误
    ISSUES = 是用来标识动态的错误
    """
    CODE = "code"  # code类型的错误
    SEND_MEG = "smg"  # 发送信息错误
    CACHE = "cache"  # 缓存相关的自定义错误
    SHOP = "shop"
    USER = "user"
    ISSUES = "issues"
    BUSINESS = "business"
    PARAMS = "params"


class Level(Enum):
    WARN = "warn"
    ERROR = "error"


class CustomError(APIException):
    """
    自定义异常的超类
    """

    def __init__(self, error: str, err_code: str, error_type: ErrorType, message: str = "", params=None,
                 level=Level.ERROR):
        super(CustomError, self).__init__()
        self.error = error
        self.error_code = err_code
        self.error_type = error_type.name
        self.level = level
        self.message = message
        self.params = params

    def __str__(self):
        m = "\n\t错误类型：" + self.error_type + \
            "\n\t错误编码：" + self.error_code + \
            "\n\t错误等级：" + self.level.name + \
            "\n\t错误信息：" + self.error + \
            "\n\t错误提示：" + self.message + "\n"
        if self.params:
            m += "\t\t" + str(self.params)
        return m

    def to_serializer(self) -> dict:
        """返回异常的序列化

        Returns:
            {
                "error_type": "smg",
                "code": "SM001",
                "error": "发送信息失败",
                "level": "error",
                "message": "",
                "params": {},
            }
        """
        return {"error_type": self.error_type,
                "error_code": self.error_code,
                "error": self.error,
                "level": self.level.name,
                "message": self.message,
                "params": self.params}

    def set_message(self, message) -> 'CustomError':
        self.message = message
        return self

    def set_params(self, params) -> 'CustomError':
        self.params = params
        return self


class CustomErrorEnum:
    """
    自定义异常的枚举类
    """

    def __new__(cls, model_name, *args, **kwargs) -> CustomError:
        """
        在实例化的一刻，就返回自定义异常
        """
        model = getattr(cls, model_name)
        return model
