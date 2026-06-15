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
