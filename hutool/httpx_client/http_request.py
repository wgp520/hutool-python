from typing import Any, Dict, Optional

import httpx


class HttpRequest:
    """HTTP请求对象，支持链式调用

    示例::

        response = (HttpRequest.get("https://example.com")
            .header("Accept", "application/json")
            .timeout(5000)
            .execute())
    """

    def __init__(self, url: str, method: str = "GET"):
        """构造HTTP请求

        :param url: 请求URL
        :param method: HTTP方法，默认GET
        """
        self._url: str = url
        self._method: str = method.upper()
        self._headers: Dict[str, str] = {}
        self._cookies: Dict[str, str] = {}
        self._form: Dict[str, str] = {}
        self._body: Optional[str] = None
        self._json_data: Any = None
        self._timeout: int = 30000  # 毫秒
        self._charset: str = "utf-8"
        self._follow_redirects: bool = True
        self._max_redirects: Optional[int] = None
        self._http_proxy: Optional[str] = None
        self._connect_timeout: Optional[int] = None
        self._read_timeout: Optional[int] = None
        self._params: Optional[Dict[str, str]] = None
        self._body_bytes: Optional[bytes] = None
        self._files: Optional[Dict[str, Any]] = None

    @classmethod
    def get(cls, url: str) -> "HttpRequest":
        """创建GET请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "GET")

    @classmethod
    def post(cls, url: str) -> "HttpRequest":
        """创建POST请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "POST")

    def method(self, method: str) -> "HttpRequest":
        """设置HTTP方法

        :param method: HTTP方法名，如GET、POST、PUT、DELETE等
        :return: 当前实例，支持链式调用
        """
        self._method = method.upper()
        return self

    def header(self, name: str, value: str) -> "HttpRequest":
        """设置单个请求头

        :param name: 请求头名称
        :param value: 请求头值
        :return: 当前实例，支持链式调用
        """
        self._headers[name] = value
        return self

    def headers(self, headers: dict) -> "HttpRequest":
        """批量设置请求头

        :param headers: 请求头字典
        :return: 当前实例，支持链式调用
        """
        self._headers.update(headers)
        return self

    def cookie(self, cookie: str) -> "HttpRequest":
        """设置Cookie

        支持格式: "name=value" 或 "name1=value1; name2=value2"

        :param cookie: Cookie字符串
        :return: 当前实例，支持链式调用
        """
        if not cookie:
            return self
        for item in cookie.split(";"):
            item = item.strip()
            if "=" in item:
                key, value = item.split("=", 1)
                self._cookies[key.strip()] = value.strip()
        return self

    def form(self, key: str, value: Optional[str] = None) -> "HttpRequest":
        """添加表单参数

        :param key: 参数名
        :param value: 参数值
        :return: 当前实例，支持链式调用
        """
        if value is not None:
            self._form[key] = value
        return self

    def body(self, body: str) -> "HttpRequest":
        """设置请求体

        :param body: 请求体字符串
        :return: 当前实例，支持链式调用
        """
        self._body = body
        return self

    def json(self, json_data: Any) -> "HttpRequest":
        """设置JSON请求体

        :param json_data: JSON可序列化的数据
        :return: 当前实例，支持链式调用
        """
        self._json_data = json_data
        return self

    def timeout(self, timeout: int) -> "HttpRequest":
        """设置超时时间（毫秒）

        :param timeout: 超时时间，单位毫秒
        :return: 当前实例，支持链式调用
        """
        self._timeout = timeout
        return self

    def charset(self, charset: str) -> "HttpRequest":
        """设置字符集

        :param charset: 字符集名称，如 utf-8、gbk 等
        :return: 当前实例，支持链式调用
        """
        self._charset = charset
        return self

    def follow_redirects(self, is_follow: bool) -> "HttpRequest":
        """设置是否跟随重定向

        :param is_follow: 是否跟随重定向
        :return: 当前实例，支持链式调用
        """
        self._follow_redirects = is_follow
        return self

    def execute(self) -> "HttpResponse":  # noqa: F821
        """执行HTTP请求

        :return: HttpResponse响应对象
        :raises httpx.HTTPStatusError: 当响应状态码表示错误时
        :raises httpx.RequestError: 当请求发生网络错误时
        """
        # 导入放在此处避免循环导入
        from .http_response import HttpResponse

        timeout_seconds = self._timeout / 1000.0

        kwargs: Dict[str, Any] = {
            "method": self._method,
            "url": self._url,
            "headers": self._headers,
            "cookies": self._cookies,
            "timeout": timeout_seconds,
            "follow_redirects": self._follow_redirects,
        }

        if self._params:
            kwargs["params"] = self._params

        if self._json_data is not None:
            kwargs["json"] = self._json_data
        elif self._body_bytes is not None:
            kwargs["content"] = self._body_bytes
        elif self._body is not None:
            kwargs["content"] = self._body.encode(self._charset)
        elif self._form:
            kwargs["data"] = self._form

        if self._files:
            kwargs["files"] = self._files

        with httpx.Client() as client:
            response = client.request(**kwargs)

        return HttpResponse(response, charset=self._charset)

    @classmethod
    def head(cls, url: str) -> "HttpRequest":
        """创建HEAD请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "HEAD")

    @classmethod
    def put(cls, url: str) -> "HttpRequest":
        """创建PUT请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "PUT")

    @classmethod
    def patch(cls, url: str) -> "HttpRequest":
        """创建PATCH请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "PATCH")

    @classmethod
    def delete(cls, url: str) -> "HttpRequest":
        """创建DELETE请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "DELETE")

    @classmethod
    def trace(cls, url: str) -> "HttpRequest":
        """创建TRACE请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "TRACE")

    @classmethod
    def options(cls, url: str) -> "HttpRequest":
        """创建OPTIONS请求

        :param url: 请求URL
        :return: HttpRequest实例
        """
        return cls(url, "OPTIONS")

    def content_type(self, ct: str) -> "HttpRequest":
        """设置Content-Type头

        :param ct: Content-Type值
        :return: 当前实例，支持链式调用
        """
        self._headers["Content-Type"] = ct
        return self

    def keep_alive(self, keep: bool) -> "HttpRequest":
        """设置Connection头

        :param keep: 是否保持连接
        :return: 当前实例，支持链式调用
        """
        self._headers["Connection"] = "keep-alive" if keep else "close"
        return self

    def basic_auth(self, username: str, password: str) -> "HttpRequest":
        """设置Basic认证

        :param username: 用户名
        :param password: 密码
        :return: 当前实例，支持链式调用
        """
        from .http_client import HttpUtil

        self._headers["Authorization"] = HttpUtil.build_basic_auth(username, password)
        return self

    def bearer_auth(self, token: str) -> "HttpRequest":
        """设置Bearer Token认证

        :param token: Bearer Token
        :return: 当前实例，支持链式调用
        """
        self._headers["Authorization"] = f"Bearer {token}"
        return self

    def body_bytes(self, data: bytes) -> "HttpRequest":
        """设置字节请求体

        :param data: 字节数据
        :return: 当前实例，支持链式调用
        """
        self._body_bytes = data
        return self

    def params(self, params: dict) -> "HttpRequest":
        """设置URL查询参数

        :param params: 参数字典
        :return: 当前实例，支持链式调用
        """
        self._params = params
        return self

    def form_file(self, name: str, file_bytes: bytes, filename: str = "file") -> "HttpRequest":
        """添加文件上传字段（记录信息供execute使用）

        :param name: 字段名
        :param file_bytes: 文件字节数据
        :param filename: 文件名
        :return: 当前实例，支持链式调用
        """
        if self._files is None:
            self._files = {}
        self._files[name] = (filename, file_bytes)
        return self

    def set_follow_redirects(self, follow: bool) -> "HttpRequest":
        """设置是否跟随重定向（与 follow_redirects 相同）。

        :param follow: 是否跟随重定向
        :return: 当前实例，支持链式调用
        """
        self._follow_redirects = follow
        return self

    def set_follow_redirects_cookie(self, follow: bool) -> "HttpRequest":
        """设置重定向时是否携带 Cookie。

        :param follow: 是否携带 Cookie
        :return: 当前实例，支持链式调用
        """
        self._follow_redirects = follow
        return self

    def set_max_redirect_count(self, count: int) -> "HttpRequest":
        """设置最大重定向次数。

        :param count: 最大重定向次数
        :return: 当前实例，支持链式调用
        """
        self._max_redirects = count
        return self

    def set_http_proxy(self, http_proxy: str) -> "HttpRequest":
        """设置 HTTP 代理。

        :param http_proxy: 代理地址，如 'http://proxy:8080'
        :return: 当前实例，支持链式调用
        """
        self._http_proxy = http_proxy
        return self

    def set_connection_timeout(self, timeout_ms: int) -> "HttpRequest":
        """设置连接超时时间（毫秒）。

        :param timeout_ms: 连接超时毫秒数
        :return: 当前实例，支持链式调用
        """
        self._connect_timeout = timeout_ms
        return self

    def set_read_timeout(self, timeout_ms: int) -> "HttpRequest":
        """设置读取超时时间（毫秒）。

        :param timeout_ms: 读取超时毫秒数
        :return: 当前实例，支持链式调用
        """
        self._read_timeout = timeout_ms
        return self
