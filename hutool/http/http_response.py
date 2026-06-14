from typing import Any, Dict, Optional

import httpx


class HttpResponse:
    """HTTP响应对象

    封装httpx.Response，提供便捷的响应数据访问方法。
    """

    def __init__(self, response: httpx.Response, charset: str = "utf-8"):
        """构造HTTP响应

        :param response: httpx响应对象
        :param charset: 字符集，默认utf-8
        """
        self._response: httpx.Response = response
        self._charset: str = charset

    @property
    def status(self) -> int:
        """获取HTTP状态码

        :return: HTTP状态码，如200、404等
        """
        return self._response.status_code

    @property
    def headers(self) -> Dict[str, str]:
        """获取响应头

        :return: 响应头字典
        """
        return dict(self._response.headers)

    @property
    def body(self) -> str:
        """获取响应体字符串

        :return: 响应体字符串
        """
        return self._response.text

    @property
    def content_length(self) -> int:
        """获取响应体长度

        :return: 响应体字节长度
        """
        content_length = self._response.headers.get("content-length")
        if content_length is not None:
            return int(content_length)
        return len(self._response.content)

    @property
    def charset(self) -> str:
        """获取字符集

        :return: 字符集名称
        """
        return self._charset

    @property
    def content_type(self) -> str:
        """获取Content-Type

        :return: Content-Type头值
        """
        return self._response.headers.get("content-type", "")

    @property
    def url(self) -> str:
        """获取最终响应的URL（考虑重定向）

        :return: 响应的URL字符串
        """
        return str(self._response.url)

    def is_ok(self) -> bool:
        """判断状态码是否为2xx（成功）

        :return: 状态码在200-299范围内返回True
        """
        return 200 <= self.status < 300

    def to_bytes(self) -> bytes:
        """获取响应体的字节数组

        :return: 响应体字节数组
        """
        return self._response.content

    def to_json(self) -> Any:
        """将响应体解析为JSON

        :return: 解析后的JSON对象（dict或list）
        :raises json.JSONDecodeError: 响应体不是有效JSON时抛出
        """
        return self._response.json()

    def to_str(self) -> str:
        """获取响应体字符串

        使用指定的字符集解码响应体。

        :return: 响应体字符串
        """
        return self._response.text

    def header(self, name: str) -> Optional[str]:
        """获取指定名称的响应头

        :param name: 响应头名称
        :return: 响应头值，不存在时返回None
        """
        return self._response.headers.get(name)

    def cookie(self, name: str) -> Optional[str]:
        """获取指定名称的Cookie值

        :param name: Cookie名称
        :return: Cookie值，不存在时返回None
        """
        return self._response.cookies.get(name)

    def __str__(self) -> str:
        """返回响应的字符串表示

        :return: 包含状态码和URL的字符串
        """
        return f"HttpResponse [status={self.status}, url={self.url}]"

    def __repr__(self) -> str:
        """返回响应的详细表示

        :return: 包含状态码和URL的字符串
        """
        return self.__str__()
