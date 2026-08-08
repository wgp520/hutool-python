import re
from typing import Dict, List, Optional, Union
from urllib.parse import parse_qs, quote, unquote

from .http_request import AsyncHttpRequest, HttpRequest


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

    @staticmethod
    def download(url: str, dest=None, timeout: int = 60000) -> Union[int, bytes]:
        """统一下载接口

        如果dest为字符串路径，下载到文件并返回字节数。
        如果dest为None，返回bytes。

        :param url: 下载URL
        :param dest: 目标文件路径或None
        :param timeout: 超时时间（毫秒）
        :return: 字节数或bytes
        """
        import httpx

        timeout_seconds = timeout / 1000.0
        if dest is not None:
            with httpx.stream("GET", url, follow_redirects=True, timeout=timeout_seconds) as response:
                response.raise_for_status()
                total = 0
                with open(dest, "wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)
                        total += len(chunk)
                return total
        else:
            response = HttpRequest.get(url).timeout(timeout).execute()
            return response.to_bytes()

    @staticmethod
    def encode_params(params: dict, charset: str = "utf-8") -> str:
        """编码参数为URL查询字符串（to_params别名）

        :param params: 参数字典
        :param charset: 字符集
        :return: URL编码后的查询字符串
        """
        return HttpUtil.to_params(params, charset)

    @staticmethod
    def get_mime_type(content_type: str) -> str:
        """从Content-Type获取MIME类型

        :param content_type: Content-Type头值
        :return: MIME类型，如 'text/html'
        """
        if not content_type:
            return ""
        return content_type.split(";")[0].strip()

    @staticmethod
    def build_basic_auth(username: str, password: str) -> str:
        """构建Basic认证头

        :param username: 用户名
        :param password: 密码
        :return: Basic认证头值（如 'Basic dXNlcjpwYXNz'）
        """
        import base64

        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return f"Basic {encoded}"

    @staticmethod
    def normalize_params(params: dict) -> dict:
        """规范化参数（过滤None值）

        :param params: 参数字典
        :return: 过滤None值后的字典
        """
        if not params:
            return {}
        return {k: v for k, v in params.items() if v is not None}


class AsyncHttpUtil:
    """异步 HTTP 工具类，提供与 :class:`HttpUtil` 完全对应的异步方法。

    与 :class:`HttpUtil` 方法名一致，所有方法均为协程，需用 ``await`` 调用。
    I/O 方法（get/post/download*）使用 ``httpx.AsyncClient`` 原生异步实现；
    纯工具方法（is_https/to_params/encode_url/create_* 等）为薄壳，直接委托同步实现。
    引入本类后通常可不再使用 :class:`HttpUtil`。

    示例::

        from hutool import AsyncHttpUtil

        html = await AsyncHttpUtil.get("https://example.com")
        await AsyncHttpUtil.download_file("https://example.com/a.zip", "/tmp/a.zip")
    """

    @staticmethod
    async def get(
        url: str,
        params: Optional[dict] = None,
        timeout: int = 30000,
        headers: Optional[dict] = None,
    ) -> str:
        """异步发送 GET 请求并返回响应体字符串。

        :param url: 请求 URL
        :param params: 查询参数
        :param timeout: 超时时间（毫秒）
        :param headers: 请求头
        :return: 响应体字符串
        """
        request = AsyncHttpRequest.get(url).timeout(timeout)
        if headers:
            request.headers(headers)
        if params:
            request._params = params
        response = await request.execute()
        return response.to_str()

    @staticmethod
    async def post(
        url: str,
        data=None,
        json_data=None,
        timeout: int = 30000,
        headers: Optional[dict] = None,
    ) -> str:
        """异步发送 POST 请求并返回响应体字符串。

        :param url: 请求 URL
        :param data: 表单数据
        :param json_data: JSON 数据
        :param timeout: 超时时间（毫秒）
        :param headers: 请求头
        :return: 响应体字符串
        """
        request = AsyncHttpRequest.post(url).timeout(timeout)
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
        response = await request.execute()
        return response.to_str()

    @staticmethod
    async def download_string(url: str, charset: str = "utf-8") -> str:
        """异步下载 URL 内容为字符串。

        :param url: 下载 URL
        :param charset: 字符集，默认 utf-8
        :return: 下载的字符串内容
        """
        response = await AsyncHttpRequest.get(url).charset(charset).execute()
        return response.to_str()

    @staticmethod
    async def download_bytes(url: str) -> bytes:
        """异步下载 URL 内容为字节数组。

        :param url: 下载 URL
        :return: 下载的字节数组
        """
        response = await AsyncHttpRequest.get(url).execute()
        return response.to_bytes()

    @staticmethod
    async def download_file(url: str, dest: str) -> int:
        """异步下载 URL 内容到文件。

        :param url: 下载 URL
        :param dest: 目标文件路径
        :return: 下载的字节数
        """
        import httpx

        total = 0
        async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client, client.stream(
            "GET", url
        ) as response:
            response.raise_for_status()
            with open(dest, "wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
                    total += len(chunk)
        return total

    @staticmethod
    async def download(url: str, dest=None, timeout: int = 60000) -> Union[int, bytes]:
        """异步统一下载接口。

        如果 dest 为字符串路径，下载到文件并返回字节数；如果 dest 为 None，返回 bytes。

        :param url: 下载 URL
        :param dest: 目标文件路径或 None
        :param timeout: 超时时间（毫秒）
        :return: 字节数或 bytes
        """
        import httpx

        timeout_seconds = timeout / 1000.0
        if dest is not None:
            total = 0
            async with httpx.AsyncClient(follow_redirects=True, timeout=timeout_seconds) as client, client.stream(
                "GET", url
            ) as response:
                response.raise_for_status()
                with open(dest, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
                        total += len(chunk)
            return total
        else:
            response = await AsyncHttpRequest.get(url).timeout(timeout).execute()
            return response.to_bytes()

    # ===================== 纯计算 / URL 工具方法（薄壳委托同步实现） =====================

    @staticmethod
    async def is_https(url: str) -> bool:
        """判断 URL 是否为 HTTPS。"""
        return HttpUtil.is_https(url)

    @staticmethod
    async def is_http(url: str) -> bool:
        """判断 URL 是否为 HTTP。"""
        return HttpUtil.is_http(url)

    @staticmethod
    async def create_get(url: str) -> HttpRequest:
        """创建 GET 请求对象（返回同步 ``HttpRequest``，可链式配置后用 ``AsyncHttpRequest`` 执行）。"""
        return HttpRequest.get(url)

    @staticmethod
    async def create_post(url: str) -> HttpRequest:
        """创建 POST 请求对象。"""
        return HttpRequest.post(url)

    @staticmethod
    async def to_params(param_map: dict, charset: str = "utf-8") -> str:
        """将参数 Map 转换为 URL 查询字符串。"""
        return HttpUtil.to_params(param_map, charset)

    @staticmethod
    async def encode_params(params: dict, charset: str = "utf-8") -> str:
        """编码参数为 URL 查询字符串（to_params 别名）。"""
        return HttpUtil.encode_params(params, charset)

    @staticmethod
    async def decode_param_map(params_str: str) -> Dict[str, str]:
        """将 URL 查询字符串解码为单值参数字典。"""
        return HttpUtil.decode_param_map(params_str)

    @staticmethod
    async def decode_params(params_str: str) -> Dict[str, List[str]]:
        """将 URL 查询字符串解码为多值参数字典。"""
        return HttpUtil.decode_params(params_str)

    @staticmethod
    async def url_with_form(url: str, form: dict) -> str:
        """将表单参数附加到 URL 上。"""
        return HttpUtil.url_with_form(url, form)

    @staticmethod
    async def get_charset(content_type: str) -> str:
        """从 Content-Type 中提取字符集。"""
        return HttpUtil.get_charset(content_type)

    @staticmethod
    async def encode_url(url_str: str) -> str:
        """URL 编码。"""
        return HttpUtil.encode_url(url_str)

    @staticmethod
    async def decode_url(url_str: str) -> str:
        """URL 解码。"""
        return HttpUtil.decode_url(url_str)

    @staticmethod
    async def get_mime_type(content_type: str) -> str:
        """从 Content-Type 获取 MIME 类型。"""
        return HttpUtil.get_mime_type(content_type)

    @staticmethod
    async def build_basic_auth(username: str, password: str) -> str:
        """构建 Basic 认证头。"""
        return HttpUtil.build_basic_auth(username, password)

    @staticmethod
    async def normalize_params(params: dict) -> dict:
        """规范化参数（过滤 None 值）。"""
        return HttpUtil.normalize_params(params)
