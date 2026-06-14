import html
from urllib.parse import quote, unquote


class EscapeUtil:
    """转义工具类，对应 Java cn.hutool.core.util.EscapeUtil"""

    # HTML特殊字符映射
    _HTML_ESCAPE_MAP = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }
    _HTML_UNESCAPE_MAP = {v: k for k, v in _HTML_ESCAPE_MAP.items()}

    @staticmethod
    def escape_html(content: str) -> str:
        """HTML转义，将 & < > " ' 转义为HTML实体

        :param content: 待转义的字符串
        :return: 转义后的字符串
        """
        if not content:
            return content
        # 先转义 & 避免二次转义
        result = content.replace("&", "&amp;")
        result = result.replace("<", "&lt;")
        result = result.replace(">", "&gt;")
        result = result.replace('"', "&quot;")
        result = result.replace("'", "&#39;")
        return result

    @staticmethod
    def unescape_html(content: str) -> str:
        """HTML反转义，将HTML实体还原为原始字符

        :param content: 待反转义的字符串
        :return: 反转义后的字符串
        """
        if not content:
            return content
        return html.unescape(content)

    @staticmethod
    def escape_xml(content: str) -> str:
        """XML转义（同HTML转义）

        :param content: 待转义的字符串
        :return: 转义后的字符串
        """
        return EscapeUtil.escape_html(content)

    @staticmethod
    def unescape_xml(content: str) -> str:
        """XML反转义（同HTML反转义）

        :param content: 待反转义的字符串
        :return: 反转义后的字符串
        """
        return EscapeUtil.unescape_html(content)

    @staticmethod
    def escape_sql(content: str) -> str:
        """SQL转义，将单引号转为两个单引号

        :param content: 待转义的字符串
        :return: 转义后的字符串
        """
        if not content:
            return content
        return content.replace("'", "''")

    @staticmethod
    def escape_url(url: str, charset: str = "utf-8") -> str:
        """URL编码

        :param url: 待编码的URL字符串
        :param charset: 字符编码，默认utf-8
        :return: 编码后的URL字符串
        """
        if not url:
            return url
        return quote(url, encoding=charset, safe="")

    @staticmethod
    def unescape_url(url: str, charset: str = "utf-8") -> str:
        """URL解码

        :param url: 待解码的URL字符串
        :param charset: 字符编码，默认utf-8
        :return: 解码后的URL字符串
        """
        if not url:
            return url
        return unquote(url, encoding=charset)
