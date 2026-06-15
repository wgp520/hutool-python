import html
import re


class HtmlUtil:
    """HTML工具类，提供HTML相关的常用处理方法"""

    # 需要被替换的HTML空白字符（制表符、换行符、回车符）
    _EMPTY_REGEX = re.compile(r"[\t\n\r]")

    @staticmethod
    def escape(html_str: str) -> str:
        """HTML转义

        将特殊字符转换为HTML实体，防止XSS攻击。
        转义规则: & -> &amp; < -> &lt; > -> &gt; " -> &quot; ' -> &#x27;

        :param html_str: 待转义的HTML字符串
        :return: 转义后的安全字符串
        """
        if html_str is None:
            return ""
        return html.escape(html_str, quote=True)

    @staticmethod
    def unescape(html_str: str) -> str:
        """HTML反转义

        将HTML实体转换回原始字符。

        :param html_str: 待反转义的HTML字符串
        :return: 反转义后的原始字符串
        """
        if html_str is None:
            return ""
        return html.unescape(html_str)

    @staticmethod
    def remove_html_tag(html_str: str) -> str:
        """移除HTML标签

        移除字符串中的所有HTML标签，只保留纯文本内容。

        :param html_str: 包含HTML标签的字符串
        :return: 移除标签后的纯文本
        """
        if html_str is None:
            return ""
        # 移除HTML注释
        text = re.sub(r"<!--.*?-->", "", html_str, flags=re.DOTALL)
        # 移除script和style标签及其内容
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        # 移除所有HTML标签
        text = re.sub(r"<[^>]+>", "", text)
        # 清理多余空白
        text = HtmlUtil._EMPTY_REGEX.sub(" ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def clean_html_tag(html_str: str) -> str:
        """清理HTML标签

        移除字符串中的所有HTML标签，只保留纯文本内容。
        本方法与 remove_html_tag 功能相同。

        :param html_str: 包含HTML标签的字符串
        :return: 清理标签后的纯文本
        """
        return HtmlUtil.remove_html_tag(html_str)

    @staticmethod
    def wrap_html(text: str) -> str:
        """包装为HTML段落

        将文本中的换行符转换为HTML的 <br> 标签，并用 <p> 标签包装。

        :param text: 纯文本字符串
        :return: 包装后的HTML段落字符串
        """
        if text is None:
            return ""
        # 转义HTML特殊字符
        escaped = html.escape(text, quote=False)
        # 将换行符替换为 <br> 标签
        escaped = escaped.replace("\n", "<br>")
        return f"<p>{escaped}</p>"
