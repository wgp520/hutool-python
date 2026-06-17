"""二维码工具类，基于qrcode"""

import base64
import io

import qrcode
from PIL import Image


class QrCodeUtil:
    """二维码工具类，基于qrcode"""

    @staticmethod
    def generate(content: str, width: int = 300, height: int = 300) -> Image.Image:
        """生成二维码，返回PIL Image对象

        :param content: 二维码内容
        :param width: 图片宽度（像素）
        :param height: 图片高度（像素）
        :return: PIL Image对象
        """
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((width, height), Image.LANCZOS)
        return img

    @staticmethod
    def generate_as_bytes(content: str, width: int = 300, height: int = 300, fmt: str = "png") -> bytes:
        """生成二维码并返回字节数组

        :param content: 二维码内容
        :param width: 图片宽度（像素）
        :param height: 图片高度（像素）
        :param fmt: 图片格式，默认为 'png'
        :return: 图片字节数组
        """
        img = QrCodeUtil.generate(content, width, height)
        buf = io.BytesIO()
        img.save(buf, format=fmt.upper())
        return buf.getvalue()

    @staticmethod
    def generate_to_file(content: str, path: str, width: int = 300, height: int = 300) -> None:
        """生成二维码并保存到文件

        :param content: 二维码内容
        :param path: 输出文件路径
        :param width: 图片宽度（像素）
        :param height: 图片高度（像素）
        """
        img = QrCodeUtil.generate(content, width, height)
        img.save(path)

    @staticmethod
    def generate_as_base64(content: str, width: int = 300, height: int = 300) -> str:
        """生成二维码的Base64编码

        :param content: 二维码内容
        :param width: 图片宽度
        :param height: 图片高度
        :return: Base64编码字符串
        """
        img_bytes = QrCodeUtil.generate_as_bytes(content, width, height)
        return base64.b64encode(img_bytes).decode("utf-8")

    @staticmethod
    def generate_as_svg(content: str, width: int = 300, height: int = 300) -> str:
        """生成SVG格式的二维码

        :param content: 二维码内容
        :param width: SVG宽度
        :param height: SVG高度
        :return: SVG格式字符串
        """
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        from qrcode.image.svg import SvgPathImage

        img = qr.make_image(image_factory=SvgPathImage)
        buf = io.BytesIO()
        img.save(buf)
        svg_str = buf.getvalue().decode("utf-8")
        # 注入宽高属性
        if 'width="' not in svg_str:
            svg_str = svg_str.replace("<svg", f'<svg width="{width}" height="{height}"', 1)
        return svg_str

    @staticmethod
    def decode(image) -> str:
        """解码二维码图片

        :param image: PIL Image对象或图片字节数据或文件路径
        :return: 二维码内容字符串
        """
        try:
            from pyzbar.pyzbar import decode as pyzbar_decode
        except ImportError:
            raise ImportError("pyzbar库未安装，请执行: pip install pyzbar")

        if isinstance(image, str):
            image = Image.open(image)
        elif isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))

        decoded = pyzbar_decode(image)
        if decoded:
            return decoded[0].data.decode("utf-8")
        return ""

    @staticmethod
    def generate_as_ascii_art(content: str, width: int = 0, height: int = 0) -> str:
        """生成 ASCII 艺术二维码。

        将二维码转为文本形式的 ASCII art。

        :param content: 二维码内容
        :param width: 图片宽度（像素），0 表示使用默认值
        :param height: 图片高度（像素），0 表示使用默认值
        :return: ASCII 艺术字符串
        """
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=1,
            border=1,
        )
        qr.add_data(content)
        qr.make(fit=True)
        matrix = qr.get_matrix()
        lines = []
        for row in matrix:
            line = ""
            for cell in row:
                line += "██" if cell else "  "
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def to_ascii_art(image) -> str:
        """将 QR 图片转为 ASCII 艺术。

        :param image: PIL Image 对象或图片文件路径
        :return: ASCII 艺术字符串
        """
        if isinstance(image, str):
            image = Image.open(image)
        # 转为灰度并缩小
        image = image.convert("L")
        image = image.resize((80, 40))
        chars = " .:-=+*#%@"
        pixels = list(image.getdata())
        lines = []
        for y in range(40):
            line = ""
            for x in range(80):
                pixel = pixels[y * 80 + x]
                idx = min(len(chars) - 1, pixel * (len(chars) - 1) // 255)
                line += chars[idx] * 2
            lines.append(line)
        return "\n".join(lines)
