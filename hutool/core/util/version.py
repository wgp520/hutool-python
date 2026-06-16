"""版本比较工具类"""

from __future__ import annotations


class VersionUtil:
    """版本比较工具类，提供版本号的比较和解析功能。"""

    @staticmethod
    def compare(version1: str, version2: str) -> int:
        """
        比较两个版本号大小。

        支持 ``"1.2.3"`` 格式，逐段比较。

        :param version1: 版本号字符串
        :param version2: 版本号字符串
        :return: 1 表示 version1 > version2，0 表示相等，-1 表示 version1 < version2
        """
        v1_parts = version1.split(".")
        v2_parts = version2.split(".")
        max_len = max(len(v1_parts), len(v2_parts))

        for i in range(max_len):
            v1 = int(v1_parts[i]) if i < len(v1_parts) else 0
            v2 = int(v2_parts[i]) if i < len(v2_parts) else 0
            if v1 > v2:
                return 1
            if v1 < v2:
                return -1

        return 0

    @staticmethod
    def is_greater(version1: str, version2: str) -> bool:
        """
        判断 version1 是否大于 version2。

        :param version1: 版本号字符串
        :param version2: 版本号字符串
        :return: 是否大于
        """
        return VersionUtil.compare(version1, version2) == 1

    @staticmethod
    def is_lower(version1: str, version2: str) -> bool:
        """
        判断 version1 是否小于 version2。

        :param version1: 版本号字符串
        :param version2: 版本号字符串
        :return: 是否小于
        """
        return VersionUtil.compare(version1, version2) == -1

    @staticmethod
    def get_main_version(version: str) -> str:
        """
        获取主版本号。

        :param version: 版本号字符串，如 ``"1.2.3"``
        :return: 主版本号，如 ``"1"``
        """
        return version.split(".")[0]

    @staticmethod
    def any_match(version: str, *candidates: str) -> bool:
        """判断版本号是否匹配候选列表中的任意一个。

        :param version: 版本号
        :param candidates: 候选版本号
        :return: 是否匹配
        """
        return any(VersionUtil.compare(version, c) == 0 for c in candidates)

    @staticmethod
    def is_greater_or_equal(version1: str, version2: str) -> bool:
        """判断 version1 是否大于等于 version2。

        :param version1: 版本号
        :param version2: 版本号
        :return: 是否大于等于
        """
        return VersionUtil.compare(version1, version2) >= 0

    @staticmethod
    def is_less_or_equal(version1: str, version2: str) -> bool:
        """判断 version1 是否小于等于 version2。

        :param version1: 版本号
        :param version2: 版本号
        :return: 是否小于等于
        """
        return VersionUtil.compare(version1, version2) <= 0
