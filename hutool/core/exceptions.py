"""异常类定义，对应 Java cn.hutool.core.exceptions。"""


class UtilException(Exception):
    """工具类通用异常。

    对应 Java cn.hutool.core.exceptions.UtilException。
    支持 format 风格的消息格式化。
    """

    def __init__(self, message: str, *args):
        if args:
            message = message.format(*args)
        super().__init__(message)


class IORuntimeException(UtilException):
    """IO 运行时异常。

    对应 Java cn.hutool.core.exceptions.IORuntimeException。
    """

    def __init__(self, message: str, *args):
        super().__init__(message, *args)


class StatefulException(UtilException):
    """有状态的异常，可携带额外状态信息。"""

    def __init__(self, message: str, *args):
        super().__init__(message, *args)


class NotInitedException(UtilException):
    """未初始化异常。"""

    def __init__(self, message: str = "Not initialized", *args):
        super().__init__(message, *args)


class NullPointerException(UtilException):
    """空指针异常。"""

    def __init__(self, message: str = "Null pointer", *args):
        super().__init__(message, *args)


class IllegalArgumentException(UtilException):
    """非法参数异常。"""

    def __init__(self, message: str, *args):
        super().__init__(message, *args)


class IllegalStateException(UtilException):
    """非法状态异常。"""

    def __init__(self, message: str, *args):
        super().__init__(message, *args)


class UnsupportedOperationException(UtilException):
    """不支持的操作异常。"""

    def __init__(self, message: str = "Unsupported operation", *args):
        super().__init__(message, *args)
