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
