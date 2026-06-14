from hutool import ArithmeticCaptcha, CaptchaUtil, LineCaptcha


class TestLineCaptcha:
    def test_create_code(self):
        captcha = LineCaptcha(100, 35, 4, 5)
        code = captcha.create_code()
        assert isinstance(code, str)
        assert len(code) > 0

    def test_verify(self):
        captcha = LineCaptcha(100, 35, 4, 5)
        code = captcha.create_code()
        assert captcha.verify(code) is True
        assert captcha.verify("wrong_code") is False

    def test_get_image_bytes(self):
        captcha = LineCaptcha(100, 35, 4, 5)
        captcha.create_code()
        img_bytes = captcha.get_image_bytes()
        assert isinstance(img_bytes, bytes)
        assert len(img_bytes) > 0


class TestArithmeticCaptcha:
    def test_create_code(self):
        captcha = ArithmeticCaptcha(100, 35)
        code = captcha.create_code()
        assert isinstance(code, str)
        assert "+" in code or "-" in code or "*" in code

    def test_get_result(self):
        captcha = ArithmeticCaptcha(100, 35)
        captcha.create_code()
        result = captcha.get_result()
        assert isinstance(result, str)

    def test_get_image_bytes(self):
        captcha = ArithmeticCaptcha(100, 35)
        captcha.create_code()
        img_bytes = captcha.get_image_bytes()
        assert isinstance(img_bytes, bytes)
        assert len(img_bytes) > 0


class TestCaptchaUtil:
    def test_create_line_captcha(self):
        captcha = CaptchaUtil.create_line_captcha(100, 35, 4, 5)
        assert isinstance(captcha, LineCaptcha)

    def test_create_arithmetic_captcha(self):
        captcha = CaptchaUtil.create_arithmetic_captcha(100, 35)
        assert isinstance(captcha, ArithmeticCaptcha)
