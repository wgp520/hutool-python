"""布尔工具类，对应 Java cn.hutool.core.util.BooleanUtil"""

from typing import Optional


class BooleanUtil:
    """布尔工具类，对应 Java cn.hutool.core.util.BooleanUtil"""

    # 用于字符串解析时判定为 True 的值（小写）
    _TRUE_STRINGS = frozenset({"true", "yes", "1", "on"})

    @staticmethod
    def is_true(bool_value: Optional[bool]) -> bool:
        """是否为 True，None 返回 False。

        :param bool_value: 待判断的布尔值
        :return: 若为 True 返回 True，否则（包括 None）返回 False
        """
        return bool_value is True

    @staticmethod
    def is_false(bool_value: Optional[bool]) -> bool:
        """是否为 False，None 返回 False。

        :param bool_value: 待判断的布尔值
        :return: 若为 False 返回 True，否则（包括 None）返回 False
        """
        return bool_value is False

    @staticmethod
    def to_int(bool_value: Optional[bool]) -> int:
        """布尔转 int，True -> 1，False -> 0，None -> 0。

        :param bool_value: 待转换的布尔值
        :return: 对应的 int 值
        """
        if bool_value is True:
            return 1
        return 0

    @staticmethod
    def int_to_boolean(int_value: Optional[int]) -> bool:
        """int 转布尔，非 0 为 True。

        :param int_value: 待转换的 int 值
        :return: 非 0 返回 True，0 或 None 返回 False
        """
        if int_value is None:
            return False
        return int_value != 0

    @staticmethod
    def and_(*values: bool) -> bool:
        """逻辑与运算，所有值均为 True 时返回 True。

        无参数时返回 True（与 Python 内置 all 行为一致）。

        :param values: 一组布尔值
        :return: 所有值均为 True 时返回 True，否则返回 False
        """
        return all(values)

    @staticmethod
    def or_(*values: bool) -> bool:
        """逻辑或运算，任一值为 True 时返回 True。

        无参数时返回 False（与 Python 内置 any 行为一致）。

        :param values: 一组布尔值
        :return: 任一值为 True 时返回 True，否则返回 False
        """
        return any(values)

    @staticmethod
    def xor(*values: bool) -> bool:
        """逻辑异或运算，奇数个 True 时返回 True。

        计算方式：对所有 True 的个数取模，奇数个 True 结果为 True。

        :param values: 一组布尔值
        :return: 奇数个 True 时返回 True，否则返回 False
        """
        count = sum(1 for v in values if v)
        return count % 2 == 1

    @staticmethod
    def negate(bool_value: bool) -> bool:
        """取反。

        :param bool_value: 待取反的布尔值
        :return: 取反后的结果
        """
        return not bool_value

    @staticmethod
    def to_str(
        bool_value: Optional[bool],
        true_str: str = "true",
        false_str: str = "false",
    ) -> str:
        """布尔转字符串。

        :param bool_value: 待转换的布尔值，None 视为 False
        :param true_str: True 对应的字符串，默认为 "true"
        :param false_str: False 对应的字符串，默认为 "false"
        :return: 对应的字符串
        """
        if bool_value is True:
            return true_str
        return false_str

    @staticmethod
    def parse(str_value: Optional[str]) -> bool:
        """字符串解析为布尔值。

        以下值（忽略大小写）解析为 True: "true", "yes", "1", "on"。
        其他所有值（包括 None）解析为 False。

        :param str_value: 待解析的字符串
        :return: 解析后的布尔值
        """
        if str_value is None:
            return False
        return str_value.strip().lower() in BooleanUtil._TRUE_STRINGS
