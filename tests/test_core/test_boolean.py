from hutool import BooleanUtil


class TestBooleanUtil:
    def test_is_true(self):
        assert BooleanUtil.is_true(True) is True
        assert BooleanUtil.is_true(False) is False

    def test_is_false(self):
        assert BooleanUtil.is_false(False) is True
        assert BooleanUtil.is_false(True) is False

    def test_to_int(self):
        assert BooleanUtil.to_int(True) == 1
        assert BooleanUtil.to_int(False) == 0

    def test_int_to_boolean(self):
        assert BooleanUtil.int_to_boolean(1) is True
        assert BooleanUtil.int_to_boolean(0) is False

    def test_and_(self):
        assert BooleanUtil.and_(True, True, True) is True
        assert BooleanUtil.and_(True, False, True) is False

    def test_or_(self):
        assert BooleanUtil.or_(False, False, True) is True
        assert BooleanUtil.or_(False, False, False) is False

    def test_xor(self):
        assert BooleanUtil.xor(True, False) is True
        assert BooleanUtil.xor(True, True) is False

    def test_negate(self):
        assert BooleanUtil.negate(True) is False
        assert BooleanUtil.negate(False) is True

    def test_to_str(self):
        assert BooleanUtil.to_str(True, "yes", "no") == "yes"
        assert BooleanUtil.to_str(False, "yes", "no") == "no"

    def test_parse(self):
        assert BooleanUtil.parse("true") is True
        assert BooleanUtil.parse("yes") is True
        assert BooleanUtil.parse("1") is True
        assert BooleanUtil.parse("on") is True
        assert BooleanUtil.parse("false") is False
        assert BooleanUtil.parse("no") is False
        assert BooleanUtil.parse("0") is False
        assert BooleanUtil.parse("anything_else") is False

    def test_to_boolean_from_bool(self):
        assert BooleanUtil.to_boolean(True) is True
        assert BooleanUtil.to_boolean(False) is False

    def test_to_boolean_from_string(self):
        assert BooleanUtil.to_boolean("true") is True
        assert BooleanUtil.to_boolean("yes") is True
        assert BooleanUtil.to_boolean("on") is True
        assert BooleanUtil.to_boolean("1") is True
        assert BooleanUtil.to_boolean("false") is False

    def test_to_boolean_from_int(self):
        assert BooleanUtil.to_boolean(1) is True
        assert BooleanUtil.to_boolean(0) is False

    def test_to_boolean_object(self):
        assert BooleanUtil.to_boolean_object("true") is True

    def test_is_boolean(self):
        assert BooleanUtil.is_boolean("true") is True
        assert BooleanUtil.is_boolean("false") is True
        assert BooleanUtil.is_boolean("yes") is True
        assert BooleanUtil.is_boolean("no") is True
        assert BooleanUtil.is_boolean("abc") is False
        assert BooleanUtil.is_boolean(None) is False

    def test_to_string_true_false(self):
        assert BooleanUtil.to_string_true_false(True) == "true"
        assert BooleanUtil.to_string_true_false(False) == "false"

    def test_to_string_yes_no(self):
        assert BooleanUtil.to_string_yes_no(True) == "yes"
        assert BooleanUtil.to_string_yes_no(False) == "no"

    def test_to_string_on_off(self):
        assert BooleanUtil.to_string_on_off(True) == "on"
        assert BooleanUtil.to_string_on_off(False) == "off"

    def test_xor_of_wrap(self):
        assert BooleanUtil.xor_of_wrap(True, False) is True
        assert BooleanUtil.xor_of_wrap(True, True) is False
        assert BooleanUtil.xor_of_wrap(False, False) is False

    def test_exactly_one_true(self):
        assert BooleanUtil.exactly_one_true(True, False, False) is True
        assert BooleanUtil.exactly_one_true(True, True, False) is False
        assert BooleanUtil.exactly_one_true(False, False, False) is False

    def test_if_true(self):
        assert BooleanUtil.if_true(True, "yes", "no") == "yes"
        assert BooleanUtil.if_true(False, "yes", "no") == "no"

    def test_negate_none(self):
        """测试 negate 对 None 输入返回 None"""
        assert BooleanUtil.negate(None) is None

    def test_to_str_with_null_str(self):
        """测试 to_str 带 null_str 参数"""
        assert BooleanUtil.to_str(None, "是", "否", "空") == "空"
        assert BooleanUtil.to_str(None, "是", "否") == "否"  # 默认 None 视为 False
        assert BooleanUtil.to_str(True, "是", "否", "空") == "是"
        assert BooleanUtil.to_str(False, "是", "否", "空") == "否"

    def test_parse_extended_true_strings(self):
        """测试扩展的 True 字符串（y, t, ok, correct, success）"""
        assert BooleanUtil.parse("y") is True
        assert BooleanUtil.parse("Y") is True
        assert BooleanUtil.parse("t") is True
        assert BooleanUtil.parse("T") is True
        assert BooleanUtil.parse("ok") is True
        assert BooleanUtil.parse("OK") is True
        assert BooleanUtil.parse("correct") is True
        assert BooleanUtil.parse("success") is True

    def test_to_boolean_extended_strings(self):
        """测试 to_boolean 扩展字符串"""
        assert BooleanUtil.to_boolean("y") is True
        assert BooleanUtil.to_boolean("ok") is True
        assert BooleanUtil.to_boolean("correct") is True
        assert BooleanUtil.to_boolean("success") is True
        assert BooleanUtil.to_boolean("t") is True

    def test_and_of_wrap(self):
        """测试 and_of_wrap，None 视为 False"""
        assert BooleanUtil.and_of_wrap(True, True) is True
        assert BooleanUtil.and_of_wrap(True, None) is False
        assert BooleanUtil.and_of_wrap(None, None) is False
        assert BooleanUtil.and_of_wrap(True, True, True) is True
        assert BooleanUtil.and_of_wrap(True, False, True) is False

    def test_or_of_wrap(self):
        """测试 or_of_wrap，None 视为 False"""
        assert BooleanUtil.or_of_wrap(True, None) is True
        assert BooleanUtil.or_of_wrap(None, None) is False
        assert BooleanUtil.or_of_wrap(False, False) is False
        assert BooleanUtil.or_of_wrap(True, False) is True

    def test_is_boolean_class(self):
        """测试 is_boolean_class 类型判断"""
        assert BooleanUtil.is_boolean_class(True) is True
        assert BooleanUtil.is_boolean_class(False) is True
        assert BooleanUtil.is_boolean_class(1) is False
        assert BooleanUtil.is_boolean_class("true") is False
        assert BooleanUtil.is_boolean_class(None) is False
