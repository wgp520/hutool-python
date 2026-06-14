"""基础类和常量，对应 Java cn.hutool.core.lang."""

from typing import Final


class DefaultParam:
    """默认参数标记类，用于区分用户传入的 None 和未传参。"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "<DEFAULT>"


# 通用常量
EMPTY: Final[str] = ""
SPACE: Final[str] = " "
TAB: Final[str] = "\t"
DOT: Final[str] = "."
SLASH: Final[str] = "/"
BACKSLASH: Final[str] = "\\"
CR: Final[str] = "\r"
LF: Final[str] = "\n"
CRLF: Final[str] = "\r\n"
COMMA: Final[str] = ","
COLON: Final[str] = ":"
SEMICOLON: Final[str] = ";"
DASH: Final[str] = "-"
UNDERLINE: Final[str] = "_"
AT: Final[str] = "@"
HASH: Final[str] = "#"
AMP: Final[str] = "&"
PIPE: Final[str] = "|"
TILDE: Final[str] = "~"
PERCENT: Final[str] = "%"
DOLLAR: Final[str] = "$"
QUESTION: Final[str] = "?"
EXCLAMATION: Final[str] = "!"
STAR: Final[str] = "*"
PLUS: Final[str] = "+"
MINUS: Final[str] = "-"
EQ: Final[str] = "="
LT: Final[str] = "<"
GT: Final[str] = ">"
NOT: Final[str] = "^"

# 常用编码
UTF_8: Final[str] = "UTF-8"
GBK: Final[str] = "GBK"
ISO_8859_1: Final[str] = "ISO-8859-1"
US_ASCII: Final[str] = "US-ASCII"

# 日期格式
NORM_DATETIME_PATTERN: Final[str] = "yyyy-MM-dd HH:mm:ss"
NORM_DATE_PATTERN: Final[str] = "yyyy-MM-dd"
NORM_TIME_PATTERN: Final[str] = "HH:mm:ss"
