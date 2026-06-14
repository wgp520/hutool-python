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
