import os
import tempfile

from hutool import ArithmeticCaptcha, CaptchaUtil, CircleCaptcha, LineCaptcha


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

    def test_line_captcha_base64(self):
        cap = LineCaptcha()
        cap.create_code()
        b64 = cap.get_image_base64()
        assert isinstance(b64, str)
        assert len(b64) > 0

    def test_line_captcha_write(self):
        cap = LineCaptcha()
        cap.create_code()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            path = f.name
        try:
            cap.write(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)


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

    def test_arithmetic_captcha_base64(self):
        cap = ArithmeticCaptcha()
        cap.create_code()
        b64 = cap.get_image_base64()
        assert isinstance(b64, str)


class TestCircleCaptcha:
    def test_circle_captcha(self):
        cap = CircleCaptcha()
        code = cap.create_code()
        assert isinstance(code, str)
        assert len(code) == 4
        assert cap.verify(code) is True
        assert cap.verify("wrong") is False
        img = cap.get_image_bytes()
        assert isinstance(img, bytes)
        assert len(img) > 0

    def test_circle_captcha_base64(self):
        cap = CircleCaptcha()
        cap.create_code()
        b64 = cap.get_image_base64()
        assert isinstance(b64, str)


class TestCaptchaUtil:
    def test_create_line_captcha(self):
        captcha = CaptchaUtil.create_line_captcha(100, 35, 4, 5)
        assert isinstance(captcha, LineCaptcha)

    def test_create_arithmetic_captcha(self):
        captcha = CaptchaUtil.create_arithmetic_captcha(100, 35)
        assert isinstance(captcha, ArithmeticCaptcha)

    def test_captcha_util_create_circle(self):
        cap = CaptchaUtil.create_circle_captcha()
        assert isinstance(cap, CircleCaptcha)
