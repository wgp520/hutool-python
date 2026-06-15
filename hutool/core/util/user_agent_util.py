"""
UserAgent 生成器工具类

随机生成各主流浏览器的 User-Agent 字符串。
纯标准库实现（random），无第三方依赖。
"""

import random as _random
import string as _string


class UserAgentUtil:
    """UserAgent 生成器，随机生成各浏览器的 User-Agent 字符串。"""

    _WINDOWS_PLATFORMS = (
        "Windows 95",
        "Windows 98",
        "Windows 98; Win 9x 4.90",
        "Windows CE",
        "Windows NT 4.0",
        "Windows NT 5.0",
        "Windows NT 5.01",
        "Windows NT 5.1",
        "Windows NT 5.2",
        "Windows NT 6.0",
        "Windows NT 6.1",
        "Windows NT 6.2",
        "Windows NT 10.0",
    )
    _LINUX_PROCESSORS = ("i686", "x86_64")
    _MAC_PROCESSORS = ("Intel", "PPC", "U; Intel", "U; PPC")
    _ANDROID_VERSIONS = (
        "1.0",
        "1.1",
        "1.5",
        "1.6",
        "2.0",
        "2.0.1",
        "2.1",
        "2.2",
        "2.2.1",
        "2.2.2",
        "2.3",
        "2.3.1",
        "2.3.3",
        "2.3.4",
        "3.0",
        "3.1",
        "3.2",
        "4.0",
        "4.0.3",
        "4.1",
        "4.2",
        "4.3",
        "4.4",
        "4.4.2",
        "5.0",
        "5.1",
        "6.0",
        "7.0",
        "8.0.0",
        "9",
        "10",
        "11",
    )
    _APPLE_DEVICES = ("iPhone", "iPad")
    _IOS_VERSIONS = (
        "3.1.3",
        "4.2.1",
        "5.1.1",
        "6.1.6",
        "7.1.2",
        "9.3.5",
        "10.3.3",
        "12.4.8",
        "14.2",
        "14.2.1",
    )

    @staticmethod
    def user_agent() -> str:
        """
        随机生成一个 User-Agent 字符串。

        随机选择 Chrome、Firefox、Safari、Opera、IE、Edge 其中之一。

        :return: User-Agent 字符串

        ::

            >>> ua = UserAgentUtil.user_agent()  # doctest: +SKIP
            >>> 'Mozilla/5.0' in ua
            True
        """
        methods = [
            UserAgentUtil.chrome,
            UserAgentUtil.firefox,
            UserAgentUtil.safari,
            UserAgentUtil.opera,
            UserAgentUtil.internet_explorer,
            UserAgentUtil.edge,
        ]
        return _random.choice(methods)()

    @staticmethod
    def chrome() -> str:
        """
        生成 Chrome 浏览器 User-Agent。

        :return: Chrome User-Agent 字符串
        """
        saf = f"{_random.randint(531, 536)}.{_random.randint(0, 2)}"
        version = _random.randint(60, 120)
        build = _random.randint(800, 899)
        bld = "".join(
            _random.choice(_string.ascii_uppercase) if c == "?" else str(_random.randint(0, 9)) for c in "##?###"
        )
        platforms = (
            f"({UserAgentUtil._linux_platform_token()}) AppleWebKit/{saf} (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Safari/{saf}",
            f"({UserAgentUtil._windows_platform_token()}) AppleWebKit/{saf} (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Safari/{saf}",
            f"({UserAgentUtil._mac_platform_token()}) AppleWebKit/{saf} (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Safari/{saf}",
            f"(Linux; {UserAgentUtil._android_platform_token()}) AppleWebKit/{saf} (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Safari/{saf}",
            f"({UserAgentUtil._ios_platform_token()}) AppleWebKit/{saf} (KHTML, like Gecko) CriOS/{version}.0.{build}.0 Mobile/{bld} Safari/{saf}",
        )
        return "Mozilla/5.0 " + _random.choice(platforms)

    @staticmethod
    def firefox() -> str:
        """
        生成 Firefox 浏览器 User-Agent。

        :return: Firefox User-Agent 字符串
        """
        ver_choices = (
            f"Gecko/20100101 Firefox/{_random.randint(4, 120)}.0",
            f"Gecko/20100101 Firefox/3.6.{_random.randint(1, 20)}",
        )
        ver = _random.choice(ver_choices)
        platforms = (
            f"({UserAgentUtil._windows_platform_token()}; en-US; rv:1.9.{_random.randint(0, 2)}.20) {ver}",
            f"({UserAgentUtil._linux_platform_token()}; rv:1.9.{_random.randint(5, 7)}.20) {ver}",
            f"({UserAgentUtil._mac_platform_token()}; rv:1.9.{_random.randint(2, 6)}.20) {ver}",
            f"({UserAgentUtil._android_platform_token()}; Mobile; rv:{_random.randint(5, 68)}.0) Gecko/{_random.randint(5, 68)}.0 Firefox/{_random.randint(5, 68)}.0",
        )
        return "Mozilla/5.0 " + _random.choice(platforms)

    @staticmethod
    def safari() -> str:
        """
        生成 Safari 浏览器 User-Agent。

        :return: Safari User-Agent 字符串
        """
        saf = f"{_random.randint(531, 535)}.{_random.randint(1, 50)}.{_random.randint(1, 7)}"
        ver = f"{_random.randint(4, 5)}.{_random.randint(0, 1)}"
        if _random.getrandbits(1):
            ver = f"{_random.randint(4, 5)}.0.{_random.randint(1, 5)}"
        platforms = (
            f"(Windows; U; {UserAgentUtil._windows_platform_token()}) AppleWebKit/{saf} (KHTML, like Gecko) Version/{ver} Safari/{saf}",
            f"({UserAgentUtil._mac_platform_token()} rv:{_random.randint(2, 6)}.0; en-US) AppleWebKit/{saf} (KHTML, like Gecko) Version/{ver} Safari/{saf}",
        )
        return "Mozilla/5.0 " + _random.choice(platforms)

    @staticmethod
    def opera() -> str:
        """
        生成 Opera 浏览器 User-Agent。

        :return: Opera User-Agent 字符串
        """
        token = (
            UserAgentUtil._linux_platform_token() if _random.getrandbits(1) else UserAgentUtil._windows_platform_token()
        )
        return f"Opera/{_random.randint(8, 9)}.{_random.randint(10, 99)}.{token} ({_random.choice(('Linux', 'Windows'))}; en-US) Presto/2.9.{_random.randint(160, 190)} Version/{_random.randint(10, 12)}.00"

    @staticmethod
    def internet_explorer() -> str:
        """
        生成 Internet Explorer User-Agent。

        :return: IE User-Agent 字符串
        """
        return f"Mozilla/5.0 (compatible; MSIE {_random.randint(5, 9)}.0; {UserAgentUtil._windows_platform_token()}; Trident/{_random.randint(3, 5)}.{_random.randint(0, 1)})"

    @staticmethod
    def edge() -> str:
        """
        生成 Edge 浏览器 User-Agent。

        :return: Edge User-Agent 字符串
        """
        saf = f"{_random.randint(531, 536)}.{_random.randint(0, 2)}"
        version = _random.randint(80, 120)
        return (
            f"Mozilla/5.0 ({UserAgentUtil._windows_platform_token()}) AppleWebKit/{saf} (KHTML, like Gecko) "
            f"Chrome/{version}.0.0.0 Safari/{saf} Edg/{version}.0.0.0"
        )

    # ---- 内部平台辅助方法 ----

    @staticmethod
    def _windows_platform_token() -> str:
        return _random.choice(UserAgentUtil._WINDOWS_PLATFORMS)

    @staticmethod
    def _linux_platform_token() -> str:
        return f"X11; Linux {_random.choice(UserAgentUtil._LINUX_PROCESSORS)}"

    @staticmethod
    def _mac_platform_token() -> str:
        return f"Macintosh; {_random.choice(UserAgentUtil._MAC_PROCESSORS)} Mac OS X 10_{_random.randint(5, 12)}_{_random.randint(0, 9)}"

    @staticmethod
    def _android_platform_token() -> str:
        return f"Android {_random.choice(UserAgentUtil._ANDROID_VERSIONS)}"

    @staticmethod
    def _ios_platform_token() -> str:
        device = _random.choice(UserAgentUtil._APPLE_DEVICES)
        ios_ver = _random.choice(UserAgentUtil._IOS_VERSIONS).replace(".", "_")
        return f"{device}; CPU {device} OS {ios_ver} like Mac OS X"
