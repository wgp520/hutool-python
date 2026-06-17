from hutool import DesensitizedUtil


class TestDesensitizedUtil:
    def test_chinese_name(self):
        result = DesensitizedUtil.chinese_name("张三丰")
        assert result == "张**" or result == "张*丰"

    def test_id_card(self):
        result = DesensitizedUtil.id_card("110101199003071234")
        assert "*" in result

    def test_mobile_phone(self):
        result = DesensitizedUtil.mobile_phone("13800138000")
        assert "138" in result
        assert "8000" in result
        assert "*" in result

    def test_fixed_phone(self):
        result = DesensitizedUtil.fixed_phone("02112345678")
        assert "*" in result

    def test_email(self):
        result = DesensitizedUtil.email("test@example.com")
        assert "@" in result
        assert "*" in result

    def test_address(self):
        result = DesensitizedUtil.address("北京市海淀区中关村大街1号", 6)
        assert "*" in result

    def test_bank_card(self):
        result = DesensitizedUtil.bank_card("6222021234567890123")
        assert "*" in result

    def test_password(self):
        result = DesensitizedUtil.password("mypassword")
        assert result == "*" * len("mypassword")

    def test_car_license(self):
        result = DesensitizedUtil.car_license("京A12345")
        assert "*" in result

    def test_ipv4(self):
        result = DesensitizedUtil.ipv4("192.168.1.1")
        assert "*" in result

    def test_license_plate(self):
        result = DesensitizedUtil.license_plate("京A12345")
        assert "*" in result

    def test_first_mask(self):
        result = DesensitizedUtil.first_mask("13800138000", mask_len=4)
        assert result.startswith("****")
        assert result.endswith("138000")

    def test_first_mask_short(self):
        result = DesensitizedUtil.first_mask("abc", mask_len=4)
        assert result == "***"

    def test_ipv6(self):
        result = DesensitizedUtil.ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        assert result.startswith("2001:0db8")
        assert "*" in result

    def test_passport(self):
        result = DesensitizedUtil.passport("E12345678")
        assert result[0] == "E"
        assert result[-1] == "8"
        assert "*" in result

    def test_credit_code(self):
        result = DesensitizedUtil.credit_code("91350100M000100Y43")
        assert result[:6] == "913501"
        assert result[-4:] == "0Y43"
        assert "*" in result

    def test_clear_mask(self):
        assert DesensitizedUtil.clear_mask("hello") == "*****"

    def test_clear_to_null(self):
        assert DesensitizedUtil.clear_to_null("hello") is None

    def test_desensitized(self):
        assert DesensitizedUtil.desensitized("1234567890", 2, 6) == "12****7890"

    def test_user_id(self):
        assert DesensitizedUtil.user_id(12345) == "1****"

    def test_user_id_short(self):
        assert DesensitizedUtil.user_id(5) == "5"
