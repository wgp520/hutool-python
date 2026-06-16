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

    @staticmethod
    def clean_empty_tag(html_str: str) -> str:
        """清除空HTML标签

        移除没有内容的HTML标签，如 <p></p>、<span>  </span> 等。

        :param html_str: HTML字符串
        :return: 清除空标签后的HTML
        """
        if html_str is None:
            return ""
        # 移除自闭合空标签 <tag /> 或 <tag></tag>（含可选空白）
        result = re.sub(r"<(\w+)(\s[^>]*)?>\s*</\1>", "", html_str, flags=re.DOTALL)
        # 再次处理嵌套的空标签
        while re.search(r"<(\w+)(\s[^>]*)?>\s*</\1>", result, flags=re.DOTALL):
            result = re.sub(r"<(\w+)(\s[^>]*)?>\s*</\1>", "", result, flags=re.DOTALL)
        return result

    @staticmethod
    def remove_html_tag_by_name(html_str: str, *tag_names) -> str:
        """移除指定名称的HTML标签（包括内容）

        :param html_str: HTML字符串
        :param tag_names: 要移除的标签名列表
        :return: 移除指定标签后的HTML
        """
        if html_str is None:
            return ""
        result = html_str
        for tag_name in tag_names:
            pattern = r"<{tag}(\s[^>]*)?>.*?</{tag}>".format(tag=re.escape(tag_name))
            result = re.sub(pattern, "", result, flags=re.DOTALL | re.IGNORECASE)
        return result

    @staticmethod
    def unwrap_html_tag(html_str: str, tag_name: str) -> str:
        """解开HTML标签保留内容

        :param html_str: HTML字符串
        :param tag_name: 标签名
        :return: 解开标签后的HTML
        """
        if html_str is None:
            return ""
        escaped_tag = re.escape(tag_name)
        # 移除开始标签
        result = re.sub(rf"<{escaped_tag}(\s[^>]*)?>", "", html_str, flags=re.IGNORECASE)
        # 移除结束标签
        result = re.sub(rf"</{escaped_tag}>", "", result, flags=re.IGNORECASE)
        return result

    @staticmethod
    def remove_html_attr(html_str: str, *attr_names) -> str:
        """移除HTML标签中的指定属性

        :param html_str: HTML字符串
        :param attr_names: 要移除的属性名列表
        :return: 移除属性后的HTML
        """
        if html_str is None:
            return ""
        result = html_str
        for attr_name in attr_names:
            # 匹配 属性名="值" 或 属性名='值' 或 属性名=值（无引号）
            pattern = r'\s+{attr}=["\'][^"\']*["\']|\s+{attr}=\S+|\s+{attr}(?=[\s/>])'.format(attr=re.escape(attr_name))
            result = re.sub(pattern, "", result, flags=re.IGNORECASE)
        return result

    @staticmethod
    def remove_all_html_attr(html_str: str) -> str:
        """移除HTML标签中的所有属性

        :param html_str: HTML字符串
        :return: 只保留标签名的HTML
        """
        if html_str is None:
            return ""
        # 将 <tag attr1="v1" attr2="v2"> 替换为 <tag>
        result = re.sub(r"<(\w+)\s+[^>]*?>", r"<\1>", html_str)
        return result
