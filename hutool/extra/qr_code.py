"""二维码工具类，基于qrcode"""

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
