"""异常类定义，对应 Java cn.hutool.core.exceptions。"""


class UtilException(Exception):
    """工具类通用异常。

    对应 Java cn.hutool.core.exceptions.UtilException。
    支持 format 风格的消息格式化。
    """

    def __init__(self, message: str, *args):
        """
        构造工具类通用异常。

        :param message: 异常消息（支持 format 格式化）
        :param args: 格式化参数
        """
        if args:
            message = message.format(*args)
        super().__init__(message)


class IORuntimeException(UtilException):
    """
    IO 运行时异常。

    对应 Java cn.hutool.core.exceptions.IORuntimeException。
    """

    def __init__(self, message: str, *args):
        """
        构造 IO 运行时异常。

        :param message: 异常消息
        :param args: 格式化参数
        """
        super().__init__(message, *args)


class StatefulException(UtilException):
    """有状态的异常，可携带额外状态信息。"""

    def __init__(self, message: str, *args):
        """
        构造有状态的异常。

        :param message: 异常消息
        :param args: 格式化参数
        """
        super().__init__(message, *args)


class NotInitedException(UtilException):
    """未初始化异常。"""

    def __init__(self, message: str = "Not initialized", *args):
        """
        构造未初始化异常。

        :param message: 异常消息，默认 "Not initialized"
        :param args: 格式化参数
        """
        super().__init__(message, *args)


class NullPointerException(UtilException):
    """空指针异常。"""

    def __init__(self, message: str = "Null pointer", *args):
        """
        构造空指针异常。

        :param message: 异常消息，默认 "Null pointer"
        :param args: 格式化参数
        """
        super().__init__(message, *args)


class IllegalArgumentException(UtilException):
    """非法参数异常。"""

    def __init__(self, message: str, *args):
        """
        构造非法参数异常。

        :param message: 异常消息
        :param args: 格式化参数
        """
        super().__init__(message, *args)


class IllegalStateException(UtilException):
    """非法状态异常。"""

    def __init__(self, message: str, *args):
        """
        构造非法状态异常。

        :param message: 异常消息
        :param args: 格式化参数
        """
        super().__init__(message, *args)


class ValidateException(IllegalArgumentException):
    """校验异常。

    对应 Java cn.hutool.core.lang.Validator.ValidateException。
    在校验方法（validate_*）失败时抛出。
    """

    def __init__(self, message: str, *args):
        """
        构造校验异常。

        :param message: 异常消息
        :param args: 格式化参数
        """
        super().__init__(message, *args)


class UnsupportedOperationException(UtilException):
    """不支持的操作异常。"""

    def __init__(self, message: str = "Unsupported operation", *args):
        """
        构造不支持的操作异常。

        :param message: 异常消息，默认 "Unsupported operation"
        :param args: 格式化参数
        """
        super().__init__(message, *args)
