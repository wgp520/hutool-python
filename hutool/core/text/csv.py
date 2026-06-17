import csv
import io
from typing import Any, Dict, List


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

    @staticmethod
    def list_to_csv(
        data: List[Dict[str, Any]],
        separator: str = "\t",
        include_header: bool = True,
    ) -> str:
        """将 list of dict 转为 CSV 字符串。

        以第一个 dict 的键作为表头。

        :param data: 字典列表
        :param separator: 分隔符，默认制表符 ``\\t``
        :param include_header: 是否包含表头行，默认 True
        :return: CSV 格式字符串

        ::

            data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
            csv_str = CsvUtil.list_to_csv(data, separator=",")
            assert "name,age" in csv_str
        """
        if not data:
            return ""
        headers = list(data[0].keys())
        f = io.StringIO()
        writer = csv.writer(f, delimiter=separator)
        if include_header:
            writer.writerow(headers)
        for row in data:
            writer.writerow([row.get(h, "") for h in headers])
        return f.getvalue()

    @staticmethod
    def write_list_to_csv(
        file_path: str,
        data: List[Dict[str, Any]],
        separator: str = ",",
        charset: str = "utf-8",
        include_header: bool = True,
    ) -> None:
        """将 list of dict 写入 CSV 文件。

        :param file_path: 目标文件路径
        :param data: 字典列表
        :param separator: 分隔符
        :param charset: 文件编码
        :param include_header: 是否包含表头行
        """
        csv_str = CsvUtil.list_to_csv(data, separator=separator, include_header=include_header)
        with open(file_path, "w", encoding=charset, newline="") as f:
            f.write(csv_str)
