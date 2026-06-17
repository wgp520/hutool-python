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

    @staticmethod
    def unescape_html_chars(content: str) -> str:
        """将常用HTML实体（&lt; &gt; &amp; &quot; &#39;）还原为原始字符。

        与 :meth:`unescape_html` 的区别在于本方法仅处理 5 个基本实体，
        不使用 ``html.unescape`` （后者会处理所有 HTML5 实体）。

        Examples::

            "&lt;p&gt;Hello &amp; World&lt;/p&gt;" -> "<p>Hello & World</p>"

        :param content: 包含HTML实体的字符串
        :return: 还原后的字符串
        """
        if not content:
            return content
        return (
            content.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", '"')
            .replace("&#39;", "'")
        )

    @staticmethod
    def escape_all(content: str) -> str:
        """转义所有非字母数字字符为 Unicode 转义序列 ``\\uXXXX``。

        :param content: 待转义的字符串
        :return: 转义后的字符串
        """
        if not content:
            return content or ""
        result = []
        for c in content:
            if c.isalnum():
                result.append(c)
            else:
                result.append(f"\\u{ord(c):04x}")
        return "".join(result)

    @staticmethod
    def safe_unescape(content: str) -> str:
        """安全反转义，失败时返回原串。

        尝试反转义 Unicode 转义序列（``\\uXXXX``），如果解析失败则返回原始字符串。

        :param content: 待反转义的字符串
        :return: 反转义后的字符串，失败返回原串
        """
        if not content:
            return content or ""
        try:
            return EscapeUtil.unescape(content)
        except Exception:
            return content

    @staticmethod
    def unescape(content: str) -> str:
        """反转义 Unicode 转义序列（``\\uXXXX``）。

        :param content: 包含 ``\\uXXXX`` 转义序列的字符串
        :return: 反转义后的字符串
        :raises ValueError: 转义序列格式非法时
        """
        if not content:
            return content or ""
        result = []
        i = 0
        while i < len(content):
            if content[i] == "\\" and i + 5 < len(content) and content[i + 1] == "u":
                hex_str = content[i + 2 : i + 6]
                try:
                    code_point = int(hex_str, 16)
                    result.append(chr(code_point))
                    i += 6
                    continue
                except ValueError:
                    pass
            result.append(content[i])
            i += 1
        return "".join(result)
