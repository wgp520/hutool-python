import re
from typing import Dict, List, Optional
from urllib.parse import parse_qs, quote, unquote

from .http_request import HttpRequest


class HttpUtil:
    """HTTP工具类，提供常用的HTTP操作方法"""

    @staticmethod
    def is_https(url: str) -> bool:
        """判断URL是否为HTTPS协议

        :param url: 待判断的URL字符串
        :return: 如果URL以 https:// 开头返回 True，否则返回 False
        """
        return url is not None and url.lower().startswith("https://")

    @staticmethod
    def is_http(url: str) -> bool:
        """判断URL是否为HTTP协议

        :param url: 待判断的URL字符串
        :return: 如果URL以 http:// 开头返回 True，否则返回 False
        """
        return url is not None and url.lower().startswith("http://")

    @staticmethod
    def get(
        url: str,
        params: Optional[dict] = None,
        timeout: int = 30000,
        headers: Optional[dict] = None,
    ) -> str:
        """发送GET请求并返回响应体字符串

        :param url: 请求URL
        :param params: 查询参数
        :param timeout: 超时时间（毫秒）
        :param headers: 请求头
        :return: 响应体字符串
        """
        request = HttpRequest.get(url).timeout(timeout)
        if headers:
            request.headers(headers)
        if params:
            request._params = params
        response = request.execute()
        return response.to_str()

    @staticmethod
    def post(
        url: str,
        data=None,
        json_data=None,
        timeout: int = 30000,
        headers: Optional[dict] = None,
    ) -> str:
        """发送POST请求并返回响应体字符串

        :param url: 请求URL
        :param data: 表单数据
        :param json_data: JSON数据
        :param timeout: 超时时间（毫秒）
        :param headers: 请求头
        :return: 响应体字符串
        """
        request = HttpRequest.post(url).timeout(timeout)
        if headers:
            request.headers(headers)
        if data is not None:
            if isinstance(data, dict):
                for k, v in data.items():
                    request.form(k, str(v))
            else:
                request.body(str(data))
        if json_data is not None:
            request.json(json_data)
        response = request.execute()
        return response.to_str()

    @staticmethod
    def create_get(url: str) -> HttpRequest:
        """创建GET请求对象

        :param url: 请求URL
        :return: HttpRequest对象
        """
        return HttpRequest.get(url)

    @staticmethod
    def create_post(url: str) -> HttpRequest:
        """创建POST请求对象

        :param url: 请求URL
        :return: HttpRequest对象
        """
        return HttpRequest.post(url)

    @staticmethod
    def download_string(url: str, charset: str = "utf-8") -> str:
        """下载URL内容为字符串

        :param url: 下载URL
        :param charset: 字符集，默认utf-8
        :return: 下载的字符串内容
        """
        response = HttpRequest.get(url).charset(charset).execute()
        return response.to_str()

    @staticmethod
    def download_file(url: str, dest: str) -> int:
        """下载URL内容到文件

        :param url: 下载URL
        :param dest: 目标文件路径
        :return: 下载的字节数
        """
        import httpx

        with httpx.stream("GET", url, follow_redirects=True, timeout=60) as response:
            response.raise_for_status()
            total = 0
            with open(dest, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
                    total += len(chunk)
            return total

    @staticmethod
    def download_bytes(url: str) -> bytes:
        """下载URL内容为字节数组

        :param url: 下载URL
        :return: 下载的字节数组
        """
        response = HttpRequest.get(url).execute()
        return response.to_bytes()

    @staticmethod
    def to_params(param_map: dict, charset: str = "utf-8") -> str:
        """将参数Map转换为URL查询字符串

        :param param_map: 参数字典
        :param charset: 字符集，默认utf-8
        :return: URL编码后的查询字符串，如 "key1=value1&key2=value2"
        """
        if not param_map:
            return ""
        encoded_pairs = []
        for key, value in param_map.items():
            encoded_key = quote(str(key), encoding=charset)
            encoded_value = quote(str(value), encoding=charset) if value is not None else ""
            encoded_pairs.append(f"{encoded_key}={encoded_value}")
        return "&".join(encoded_pairs)

    @staticmethod
    def decode_param_map(params_str: str) -> Dict[str, str]:
        """将URL查询字符串解码为单值参数字典

        如果某个键对应多个值，只取第一个值。

        :param params_str: URL查询字符串，如 "key1=value1&key2=value2"
        :return: 参数字典，值为单个字符串
        """
        if not params_str:
            return {}
        result: Dict[str, str] = {}
        parsed = parse_qs(params_str, keep_blank_values=True)
        for key, values in parsed.items():
            result[key] = values[0] if values else ""
        return result

    @staticmethod
    def decode_params(params_str: str) -> Dict[str, List[str]]:
        """将URL查询字符串解码为多值参数字典

        :param params_str: URL查询字符串，如 "key=value1&key=value2"
        :return: 参数字典，值为字符串列表
        """
        if not params_str:
            return {}
        return parse_qs(params_str, keep_blank_values=True)

    @staticmethod
    def url_with_form(url: str, form: dict) -> str:
        """将表单参数附加到URL上

        :param url: 基础URL
        :param form: 表单参数字典
        :return: 附加参数后的完整URL
        """
        if not form:
            return url
        params_str = HttpUtil.to_params(form)
        if "?" in url:
            if url.endswith("&") or url.endswith("?"):
                return url + params_str
            return url + "&" + params_str
        return url + "?" + params_str

    @staticmethod
    def get_charset(content_type: str) -> str:
        """从Content-Type中提取字符集

        :param content_type: Content-Type头值，如 "text/html; charset=utf-8"
        :return: 字符集名称，如 "utf-8"；如果未指定则返回 "utf-8"
        """
        if not content_type:
            return "utf-8"
        match = re.search(r"charset\s*=\s*([^\s;]+)", content_type, re.IGNORECASE)
        if match:
            return match.group(1).strip().strip('"').strip("'")
        return "utf-8"

    @staticmethod
    def encode_url(url_str: str) -> str:
        """URL编码

        :param url_str: 待编码的URL字符串
        :return: 编码后的URL字符串
        """
        if not url_str:
            return ""
        return quote(url_str, safe=":/?#[]@!$&'()*+,;=-._~%")

    @staticmethod
    def decode_url(url_str: str) -> str:
        """URL解码

        :param url_str: 待解码的URL字符串
        :return: 解码后的URL字符串
        """
        if not url_str:
            return ""
        return unquote(url_str)
