import base64
import io
import random
import string

from PIL import Image, ImageDraw, ImageFont


class LineCaptcha:
    """线段干扰验证码。

    在图片上绘制随机字符，并添加随机干扰线段以增加识别难度。
    """

    def __init__(self, width: int = 100, height: int = 35, code_count: int = 4, line_count: int = 5) -> None:
        """初始化线段干扰验证码。

        :param width: 图片宽度，默认100像素
        :param height: 图片高度，默认35像素
        :param code_count: 验证码字符个数，默认4
        :param line_count: 干扰线条数，默认5
        """
        self._width: int = width
        self._height: int = height
        self._code_count: int = code_count
        self._line_count: int = line_count
        self._code: str = ""

    def create_code(self) -> str:
        """生成随机验证码字符串并绘制验证码图片。

        :return: 生成的验证码字符串
        """
        chars = string.ascii_letters + string.digits
        self._code = "".join(random.choices(chars, k=self._code_count))
        return self._code

    def verify(self, code: str) -> bool:
        """校验输入的验证码是否正确（不区分大小写）。

        :param code: 用户输入的验证码
        :return: 验证成功返回True，否则返回False
        """
        if not self._code or not code:
            return False
        return self._code.lower() == code.lower()

    def get_image_bytes(self, fmt: str = "png") -> bytes:
        """生成验证码图片的字节数据。

        :param fmt: 图片格式，默认"png"
        :return: 图片的字节数据
        """
        if not self._code:
            self.create_code()

        img = Image.new("RGB", (self._width, self._height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # 尝试加载字体，失败则使用默认字体
        try:
            font = ImageFont.truetype("arial.ttf", size=int(self._height * 0.6))
        except OSError:
            font = ImageFont.load_default()

        # 绘制验证码字符
        char_width = self._width // (self._code_count + 1)
        for i, ch in enumerate(self._code):
            x = char_width * i + random.randint(2, 8)
            y = random.randint(0, max(1, self._height // 4))
            color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
            draw.text((x, y), ch, fill=color, font=font)

        # 绘制干扰线
        for _ in range(self._line_count):
            x1 = random.randint(0, self._width)
            y1 = random.randint(0, self._height)
            x2 = random.randint(0, self._width)
            y2 = random.randint(0, self._height)
            color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=1)

        buf = io.BytesIO()
        img.save(buf, format=fmt)
        return buf.getvalue()

    def get_image_base64(self, fmt: str = "png") -> str:
        """获取验证码图片的Base64编码

        :param fmt: 图片格式，默认"png"
        :return: Base64编码字符串
        """
        image_bytes = self.get_image_bytes(fmt)
        return base64.b64encode(image_bytes).decode("utf-8")

    def write(self, path: str, fmt: str = "png") -> None:
        """将验证码图片写入文件

        :param path: 输出文件路径
        :param fmt: 图片格式，默认"png"
        """
        image_bytes = self.get_image_bytes(fmt)
        with open(path, "wb") as f:
            f.write(image_bytes)


class ArithmeticCaptcha:
    """算术验证码。

    生成简单的数学表达式（如"3+5=?"），用户需计算结果。
    """

    def __init__(self, width: int = 100, height: int = 35) -> None:
        """初始化算术验证码。

        :param width: 图片宽度，默认100像素
        :param height: 图片高度，默认35像素
        """
        self._width: int = width
        self._height: int = height
        self._expression: str = ""
        self._result: str = ""

    def create_code(self) -> str:
        """生成随机算术表达式，并计算结果。

        :return: 生成的算术表达式（如"3+5=?"）
        """
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])

        if op == "+":
            result = a + b
        elif op == "-":
            # 确保结果非负
            if a < b:
                a, b = b, a
                result = a - b
            else:
                result = a - b
        else:
            result = a * b

        self._expression = f"{a}{op}{b}=?"
        self._result = str(result)
        return self._expression

    def get_result(self) -> str:
        """获取算术表达式的正确结果。

        :return: 表达式结果字符串
        """
        return self._result

    def verify(self, code: str) -> bool:
        """校验用户输入的答案是否正确。

        :param code: 用户输入的答案
        :return: 答案正确返回True，否则返回False
        """
        if not self._result or not code:
            return False
        return self._result == code.strip()

    def get_image_bytes(self, fmt: str = "png") -> bytes:
        """生成验证码图片的字节数据。

        :param fmt: 图片格式，默认"png"
        :return: 图片的字节数据
        """
        if not self._expression:
            self.create_code()

        img = Image.new("RGB", (self._width, self._height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", size=int(self._height * 0.5))
        except OSError:
            font = ImageFont.load_default()

        # 计算文字居中位置
        bbox = draw.textbbox((0, 0), self._expression, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self._width - text_width) // 2
        y = (self._height - text_height) // 2

        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        draw.text((x, y), self._expression, fill=color, font=font)

        # 绘制干扰线
        for _ in range(3):
            x1 = random.randint(0, self._width)
            y1 = random.randint(0, self._height)
            x2 = random.randint(0, self._width)
            y2 = random.randint(0, self._height)
            line_color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
            draw.line([(x1, y1), (x2, y2)], fill=line_color, width=1)

        buf = io.BytesIO()
        img.save(buf, format=fmt)
        return buf.getvalue()

    def get_image_base64(self, fmt: str = "png") -> str:
        """获取验证码图片的Base64编码

        :param fmt: 图片格式，默认"png"
        :return: Base64编码字符串
        """
        image_bytes = self.get_image_bytes(fmt)
        return base64.b64encode(image_bytes).decode("utf-8")

    def write(self, path: str, fmt: str = "png") -> None:
        """将验证码图片写入文件

        :param path: 输出文件路径
        :param fmt: 图片格式，默认"png"
        """
        image_bytes = self.get_image_bytes(fmt)
        with open(path, "wb") as f:
            f.write(image_bytes)


class CircleCaptcha:
    """圆干扰验证码

    在图片上绘制随机字符，并添加随机圆圈干扰。
    """

    def __init__(self, width: int = 100, height: int = 35, code_count: int = 4, circle_count: int = 3) -> None:
        """初始化圆干扰验证码。

        :param width: 图片宽度，默认100像素
        :param height: 图片高度，默认35像素
        :param code_count: 验证码字符个数，默认4
        :param circle_count: 干扰圆圈数，默认3
        """
        self._width = width
        self._height = height
        self._code_count = code_count
        self._circle_count = circle_count
        self._code = ""

    def create_code(self) -> str:
        """生成随机验证码字符串并绘制验证码图片。

        :return: 生成的验证码字符串
        """
        chars = string.ascii_letters + string.digits
        self._code = "".join(random.choices(chars, k=self._code_count))
        return self._code

    def verify(self, code: str) -> bool:
        """校验输入的验证码是否正确（不区分大小写）。

        :param code: 用户输入的验证码
        :return: 验证成功返回True，否则返回False
        """
        if not self._code or not code:
            return False
        return self._code.lower() == code.lower()

    def get_image_bytes(self, fmt: str = "png") -> bytes:
        """生成验证码图片的字节数据。

        :param fmt: 图片格式，默认"png"
        :return: 图片的字节数据
        """
        if not self._code:
            self.create_code()

        img = Image.new("RGB", (self._width, self._height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", size=int(self._height * 0.6))
        except OSError:
            font = ImageFont.load_default()

        # 绘制验证码字符
        char_width = self._width // (self._code_count + 1)
        for i, ch in enumerate(self._code):
            x = char_width * i + random.randint(2, 8)
            y = random.randint(0, max(1, self._height // 4))
            color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
            draw.text((x, y), ch, fill=color, font=font)

        # 绘制干扰圆圈
        for _ in range(self._circle_count):
            cx = random.randint(0, self._width)
            cy = random.randint(0, self._height)
            r = random.randint(5, max(6, min(self._width, self._height) // 3))
            color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=color, width=1)

        buf = io.BytesIO()
        img.save(buf, format=fmt)
        return buf.getvalue()

    def get_image_base64(self, fmt: str = "png") -> str:
        """获取验证码图片的Base64编码

        :param fmt: 图片格式，默认"png"
        :return: Base64编码字符串
        """
        image_bytes = self.get_image_bytes(fmt)
        return base64.b64encode(image_bytes).decode("utf-8")

    def write(self, path: str, fmt: str = "png") -> None:
        """将验证码图片写入文件

        :param path: 输出文件路径
        :param fmt: 图片格式，默认"png"
        """
        image_bytes = self.get_image_bytes(fmt)
        with open(path, "wb") as f:
            f.write(image_bytes)


class CaptchaUtil:
    """验证码工厂类。

    提供各种验证码的便捷创建方法。
    """

    @staticmethod
    def create_line_captcha(
        width: int = 100, height: int = 35, code_count: int = 4, line_count: int = 5
    ) -> LineCaptcha:
        """创建线段干扰验证码。

        :param width: 图片宽度，默认100像素
        :param height: 图片高度，默认35像素
        :param code_count: 验证码字符个数，默认4
        :param line_count: 干扰线条数，默认5
        :return: LineCaptcha实例
        """
        return LineCaptcha(width, height, code_count, line_count)

    @staticmethod
    def create_arithmetic_captcha(width: int = 100, height: int = 35) -> ArithmeticCaptcha:
        """创建算术验证码。

        :param width: 图片宽度，默认100像素
        :param height: 图片高度，默认35像素
        :return: ArithmeticCaptcha实例
        """
        return ArithmeticCaptcha(width, height)

    @staticmethod
    def create_circle_captcha(
        width: int = 100, height: int = 35, code_count: int = 4, circle_count: int = 3
    ) -> CircleCaptcha:
        """创建圆干扰验证码。

        :param width: 图片宽度，默认100像素
        :param height: 图片高度，默认35像素
        :param code_count: 验证码字符个数，默认4
        :param circle_count: 干扰圆圈数，默认3
        :return: CircleCaptcha实例
        """
        return CircleCaptcha(width, height, code_count, circle_count)
