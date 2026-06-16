from hutool import PhoneUtil


class TestPhoneUtil:
    def test_is_mobile(self):
        assert PhoneUtil.is_mobile("13800138000") is True
        assert PhoneUtil.is_mobile("12345678901") is False
        assert PhoneUtil.is_mobile("1380013800") is False

    def test_is_mobile_hk(self):
        assert PhoneUtil.is_mobile_hk("51234567") is True

    def test_is_mobile_tw(self):
        assert PhoneUtil.is_mobile_tw("0912345678") is True

    def test_is_mobile_mo(self):
        assert PhoneUtil.is_mobile_mo("66123456") is True

    def test_is_phone(self):
        assert PhoneUtil.is_phone("13800138000") is True
        assert PhoneUtil.is_phone("02112345678") is True

    def test_hide_before(self):
        result = PhoneUtil.hide_before("13800138000")
        assert result.endswith("8000")
        assert "*" in result

    def test_hide_between(self):
        result = PhoneUtil.hide_between("13800138000")
        assert result.startswith("138")
        assert result.endswith("8000")
        assert "*" in result

    def test_hide_after(self):
        result = PhoneUtil.hide_after("13800138000")
        assert result.startswith("1380")
        assert "*" in result

    def test_sub_before(self):
        result = PhoneUtil.sub_before("13800138000")
        assert result == "138"

    def test_sub_after(self):
        result = PhoneUtil.sub_after("13800138000")
        assert result == "8000"

    def test_is_mobile_simple(self):
        assert PhoneUtil.is_mobile_simple("13800138000") is True
        assert PhoneUtil.is_mobile_simple("10000000000") is True
        assert PhoneUtil.is_mobile_simple("23800138000") is False  # 不是1开头
        assert PhoneUtil.is_mobile_simple("1380013800") is False  # 10位
        assert PhoneUtil.is_mobile_simple("138001380001") is False  # 12位
        assert PhoneUtil.is_mobile_simple("") is False
        assert PhoneUtil.is_mobile_simple(None) is False

    def test_is_tel(self):
        assert PhoneUtil.is_tel("010-12345678") is True
        assert PhoneUtil.is_tel("021-87654321") is True
        assert PhoneUtil.is_tel("13800138000") is False

    def test_is_tel_400_800(self):
        assert PhoneUtil.is_tel_400_800("4001234567") is True
        assert PhoneUtil.is_tel_400_800("8001234567") is True
        assert PhoneUtil.is_tel_400_800("9001234567") is False
        assert PhoneUtil.is_tel_400_800(None) is False

    def test_sub_between(self):
        assert PhoneUtil.sub_between("13800138000", 3, 7) == "0013"
        assert PhoneUtil.sub_between("", 0, 3) == ""

    def test_sub_tel_before(self):
        assert PhoneUtil.sub_tel_before("010-12345678") == "010"
        assert PhoneUtil.sub_tel_before("021-87654321") == "021"
        assert PhoneUtil.sub_tel_before("") == ""

    def test_sub_tel_after(self):
        assert PhoneUtil.sub_tel_after("010-12345678") == "12345678"
        assert PhoneUtil.sub_tel_after("") == ""
