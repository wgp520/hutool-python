import re
from typing import Dict, List
from urllib.parse import parse_qs, parse_qsl, quote, unquote, urlencode, urlparse


class URLUtil:
    """URL工具类，对应 Java cn.hutool.core.util.URLUtil"""

    @staticmethod
    def normalize(url_str: str) -> str:
        """标准化URL，补齐协议头

        如果URL缺少协议头（http:// 或 https://），自动补充 http://。

        :param url_str: 原始URL字符串
        :return: 标准化后的URL字符串
        """
        if not url_str:
            return url_str
        url_str = url_str.strip()
        if not re.match(r"^[a-zA-Z]+://", url_str):
            url_str = "http://" + url_str
        return url_str

    @staticmethod
    def encode(url_str: str, charset: str = "utf-8") -> str:
        """URL编码

        对整个URL字符串进行编码。

        :param url_str: 待编码的URL字符串
        :param charset: 字符编码，默认utf-8
        :return: 编码后的URL字符串
        """
        if not url_str:
            return url_str
        return quote(url_str, encoding=charset, safe=":/?#[]@!$&'()*+,;=-._~%")

    @staticmethod
    def decode(url_str: str, charset: str = "utf-8") -> str:
        """URL解码

        对URL编码的字符串进行解码。

        :param url_str: 待解码的URL字符串
        :param charset: 字符编码，默认utf-8
        :return: 解码后的URL字符串
        """
        if not url_str:
            return url_str
        return unquote(url_str, encoding=charset)

    @staticmethod
    def encode_params(params_str: str, charset: str = "utf-8") -> str:
        """编码URL参数部分

        对URL查询参数字符串中的值部分进行编码。

        :param params_str: 参数字符串，如 "key1=value1&key2=value2"
        :param charset: 字符编码，默认utf-8
        :return: 编码后的参数字符串
        """
        if not params_str:
            return params_str
        pairs = parse_qsl(params_str, keep_blank_values=True)
        encoded_pairs = []
        for key, value in pairs:
            encoded_key = quote(key, encoding=charset, safe="")
            encoded_value = quote(value, encoding=charset, safe="")
            encoded_pairs.append(f"{encoded_key}={encoded_value}")
        return "&".join(encoded_pairs)

    @staticmethod
    def get_path(url_str: str) -> str:
        """获取URL的路径部分

        :param url_str: URL字符串
        :return: URL的路径部分，解析失败返回空字符串
        """
        if not url_str:
            return ""
        try:
            parsed = urlparse(url_str)
            return parsed.path
        except Exception:
            return ""

    @staticmethod
    def get_host(url_str: str) -> str:
        """获取URL的主机部分

        :param url_str: URL字符串
        :return: URL的主机名，解析失败返回空字符串
        """
        if not url_str:
            return ""
        try:
            parsed = urlparse(url_str)
            return parsed.hostname or ""
        except Exception:
            return ""

    @staticmethod
    def get_port(url_str: str) -> int:
        """获取URL的端口号，无端口返回-1

        :param url_str: URL字符串
        :return: 端口号，无端口或解析失败返回-1
        """
        if not url_str:
            return -1
        try:
            parsed = urlparse(url_str)
            return parsed.port if parsed.port is not None else -1
        except Exception:
            return -1

    @staticmethod
    def get_query(url_str: str) -> str:
        """获取URL的查询参数部分

        :param url_str: URL字符串
        :return: URL的查询参数字符串（不含?），解析失败返回空字符串
        """
        if not url_str:
            return ""
        try:
            parsed = urlparse(url_str)
            return parsed.query
        except Exception:
            return ""

    @staticmethod
    def build_url(base: str, params: Dict[str, str]) -> str:
        """构建带参数的URL

        在基础URL上附加参数，如果原URL已有参数则追加。

        :param base: 基础URL
        :param params: 参数字典
        :return: 带参数的完整URL
        """
        if not base:
            return ""
        if not params:
            return base

        param_str = urlencode(params, encoding="utf-8")
        separator = "&" if "?" in base else "?"
        return f"{base}{separator}{param_str}"

    @staticmethod
    def url_with_form(url: str, form: Dict[str, str]) -> str:
        """在URL后附加表单参数

        与build_url类似，将表单参数附加到URL后。

        :param url: 原始URL
        :param form: 表单参数字典
        :return: 附加参数后的URL
        """
        return URLUtil.build_url(url, form)

    @staticmethod
    def to_params(param_map: Dict[str, str], charset: str = "utf-8") -> str:
        """参数Map转URL参数字符串

        :param param_map: 参数字典
        :param charset: 字符编码，默认utf-8
        :return: URL参数字符串，如 "key1=value1&key2=value2"
        """
        if not param_map:
            return ""
        return urlencode(param_map, encoding=charset)

    @staticmethod
    def decode_param_map(params_str: str, charset: str = "utf-8") -> Dict[str, str]:
        """URL参数字符串转Map（每个key只保留最后一个值）

        :param params_str: 参数字符串，如 "key1=value1&key2=value2"
        :param charset: 字符编码，默认utf-8
        :return: 参数字典，重复key时保留最后一个值
        """
        if not params_str:
            return {}
        pairs = parse_qsl(params_str, keep_blank_values=True, encoding=charset)
        result: Dict[str, str] = {}
        for key, value in pairs:
            result[key] = value
        return result

    @staticmethod
    def decode_params(params_str: str, charset: str = "utf-8") -> Dict[str, List[str]]:
        """URL参数字符串转Map（每个key对应值列表）

        :param params_str: 参数字符串，如 "key=value1&key=value2"
        :param charset: 字符编码，默认utf-8
        :return: 参数字典，每个key对应一个值列表
        """
        if not params_str:
            return {}
        return parse_qs(params_str, keep_blank_values=True, encoding=charset)

    @staticmethod
    def is_https(url_str: str) -> bool:
        """是否为HTTPS

        :param url_str: URL字符串
        :return: 是HTTPS返回True，否则返回False
        """
        if not url_str:
            return False
        try:
            parsed = urlparse(url_str)
            return parsed.scheme.lower() == "https"
        except Exception:
            return False

    @staticmethod
    def is_http(url_str: str) -> bool:
        """是否为HTTP

        :param url_str: URL字符串
        :return: 是HTTP返回True，否则返回False
        """
        if not url_str:
            return False
        try:
            parsed = urlparse(url_str)
            return parsed.scheme.lower() == "http"
        except Exception:
            return False

    @staticmethod
    def build_query(params: Dict[str, str], is_encode: bool = True) -> str:
        """将参数字典转换为查询字符串。

        :param params: 参数字典
        :param is_encode: 是否 URL 编码
        :return: 查询字符串
        """
        if not params:
            return ""
        if is_encode:
            return urlencode(params, encoding="utf-8")
        return "&".join(f"{k}={v}" for k, v in params.items())

    @staticmethod
    def encode_blank(url: str) -> str:
        """编码 URL 中的空格（替换为 %20）。

        :param url: URL 字符串
        :return: 编码后的 URL
        """
        if not url:
            return url
        return url.replace(" ", "%20")

    @staticmethod
    def complete_url(base_url: str, relative_path: str) -> str:
        """补全相对 URL。

        :param base_url: 基础 URL
        :param relative_path: 相对路径
        :return: 完整 URL
        """
        from urllib.parse import urljoin

        return urljoin(base_url, relative_path)

    @staticmethod
    def get_params(url: str) -> Dict[str, str]:
        """解析 URL 参数为字典。

        :param url: URL 字符串
        :return: 参数字典
        """
        try:
            parsed = urlparse(url)
            return URLUtil.decode_param_map(parsed.query)
        except Exception:
            return {}
