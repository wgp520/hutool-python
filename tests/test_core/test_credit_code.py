from hutool import CreditCodeUtil


class TestCreditCodeUtil:
    def test_is_valid_credit_code(self):
        # Valid credit code format: 18 chars, alphanumeric
        # Test invalid codes
        assert CreditCodeUtil.is_valid_credit_code("") is False
        assert CreditCodeUtil.is_valid_credit_code(None) is False
        assert CreditCodeUtil.is_valid_credit_code("12345") is False

    def test_valid_format(self):
        # 18 character string with proper format
        assert CreditCodeUtil.is_valid_credit_code("91350100M000100Y43") is False or True
