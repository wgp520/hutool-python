import csv
import io
from typing import List


class CsvUtil:
    """CSV工具类"""

    @staticmethod
    def read(path: str, charset: str = "utf-8") -> List[List[str]]:
        """读取CSV文件为二维列表

        :param path: CSV文件路径
        :param charset: 文件编码，默认utf-8
        :return: 二维列表，每个元素为一行的数据
        """
        with open(path, encoding=charset, newline="") as f:
            reader = csv.reader(f)
            return [row for row in reader]

    @staticmethod
    def read_string(csv_str: str) -> List[List[str]]:
        """读取CSV字符串为二维列表

        :param csv_str: CSV格式的字符串
        :return: 二维列表，每个元素为一行的数据
        """
        f = io.StringIO(csv_str)
        reader = csv.reader(f)
        return [row for row in reader]

    @staticmethod
    def write(path: str, data: List[List[str]], charset: str = "utf-8") -> None:
        """写入CSV文件

        :param path: CSV文件路径
        :param data: 二维列表数据
        :param charset: 文件编码，默认utf-8
        """
        with open(path, "w", encoding=charset, newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    @staticmethod
    def write_string(data: List[List[str]]) -> str:
        """将二维列表转为CSV字符串

        :param data: 二维列表数据
        :return: CSV格式的字符串
        """
        f = io.StringIO()
        writer = csv.writer(f)
        writer.writerows(data)
        return f.getvalue()
