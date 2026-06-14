"""版本比较工具类"""

from __future__ import annotations


class VersionUtil:
    """版本比较工具类"""

    @staticmethod
    def compare(version1: str, version2: str) -> int:
        """比较两个版本号，1: v1>v2, 0: 相等, -1: v1<v2
        支持 "1.2.3" 格式
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
        """version1是否大于version2"""
        return VersionUtil.compare(version1, version2) == 1

    @staticmethod
    def is_lower(version1: str, version2: str) -> bool:
        """version1是否小于version2"""
        return VersionUtil.compare(version1, version2) == -1

    @staticmethod
    def get_main_version(version: str) -> str:
        """获取主版本号，如 "1.2.3" -> "1" """
        return version.split(".")[0]
