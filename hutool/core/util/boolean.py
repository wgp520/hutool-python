"""布尔工具类，对应 Java cn.hutool.core.util.BooleanUtil"""

from typing import Any, Optional


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

    @staticmethod
    def to_boolean(value: Any) -> bool:
        """
        将值转为布尔值。

        以下值解析为 True: ``True``, ``"true"``, ``"yes"``, ``"on"``, ``"1"``, ``1``。
        其他值返回 False。

        :param value: 待转换的值
        :return: 布尔值
        """
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return value != 0
        if isinstance(value, str):
            return value.strip().lower() in BooleanUtil._TRUE_STRINGS
        return bool(value)

    @staticmethod
    def to_boolean_object(value: Any) -> bool:
        """
        与 :meth:`to_boolean` 相同。

        :param value: 待转换的值
        :return: 布尔值
        """
        return BooleanUtil.to_boolean(value)

    @staticmethod
    def is_boolean(s: Optional[str]) -> bool:
        """
        判断字符串是否为布尔字符串（``"true"``, ``"false"``, ``"yes"``, ``"no"``, ``"on"``, ``"off"``, ``"1"``, ``"0"``）。

        :param s: 待检查的字符串
        :return: 是否为布尔字符串
        """
        if s is None:
            return False
        return s.strip().lower() in {"true", "false", "yes", "no", "on", "off", "1", "0"}

    @staticmethod
    def to_string_true_false(bool_value: Optional[bool]) -> str:
        """
        布尔转 "true"/"false"。

        :param bool_value: 布尔值
        :return: "true" 或 "false"
        """
        return "true" if bool_value is True else "false"

    @staticmethod
    def to_string_yes_no(bool_value: Optional[bool]) -> str:
        """
        布尔转 "yes"/"no"。

        :param bool_value: 布尔值
        :return: "yes" 或 "no"
        """
        return "yes" if bool_value is True else "no"

    @staticmethod
    def to_string_on_off(bool_value: Optional[bool]) -> str:
        """
        布尔转 "on"/"off"。

        :param bool_value: 布尔值
        :return: "on" 或 "off"
        """
        return "on" if bool_value is True else "off"

    @staticmethod
    def xor_of_wrap(a: bool, b: bool) -> bool:
        """
        两个布尔值的异或运算。

        :param a: 第一个布尔值
        :param b: 第二个布尔值
        :return: 异或结果
        """
        return a != b

    @staticmethod
    def exactly_one_true(*values: bool) -> bool:
        """
        判断是否恰好有一个 True。

        :param values: 布尔值列表
        :return: 恰好一个 True 时返回 True
        """
        return sum(1 for v in values if v) == 1

    @staticmethod
    def if_true(condition: bool, true_val: Any, false_val: Any) -> Any:
        """
        三元表达式。

        :param condition: 条件
        :param true_val: 为 True 时的返回值
        :param false_val: 为 False 时的返回值
        :return: 条件对应的值
        """
        return true_val if condition else false_val
