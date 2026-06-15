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
        self._params: Optional[Dict[str, str]] = None

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
        elif self._body is not None:
            kwargs["content"] = self._body.encode(self._charset)
        elif self._form:
            kwargs["data"] = self._form

        with httpx.Client() as client:
            response = client.request(**kwargs)

        return HttpResponse(response, charset=self._charset)
