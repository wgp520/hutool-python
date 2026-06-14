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
