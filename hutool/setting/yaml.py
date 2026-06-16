"""YAML工具类"""

import os
from typing import Any, Optional

import yaml


class YamlUtil:
    """YAML工具类"""

    @staticmethod
    def load(path: str) -> Any:
        """加载YAML文件

        :param path: YAML文件路径
        :return: 解析后的Python对象（dict、list等）
        """
        path = os.path.abspath(path)
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_by_string(yaml_str: str) -> Any:
        """从字符串加载YAML

        :param yaml_str: YAML格式的字符串
        :return: 解析后的Python对象（dict、list等）
        """
        return yaml.safe_load(yaml_str)

    @staticmethod
    def dump(data: Any, path: Optional[str] = None) -> str:
        """将数据序列化为YAML格式

        :param data: 待序列化的Python对象
        :param path: 输出文件路径，为None时不写文件
        :return: YAML格式的字符串
        """
        result = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        if path is not None:
            path = os.path.abspath(path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(result)
        return result

    @staticmethod
    def dump_to(data, stream) -> None:
        """将数据序列化为YAML并写入流

        :param data: Python对象
        :param stream: 文件对象
        """
        yaml.dump(data, stream, allow_unicode=True, default_flow_style=False, sort_keys=False)

    @staticmethod
    def load_as_dict(path: str) -> dict:
        """加载YAML为字典

        :param path: YAML文件路径
        :return: 字典
        """
        result = YamlUtil.load(path)
        if not isinstance(result, dict):
            raise TypeError(f"YAML文件内容不是字典类型，实际类型: {type(result).__name__}")
        return result

    @staticmethod
    def load_as_list(path: str) -> list:
        """加载YAML为列表

        :param path: YAML文件路径
        :return: 列表
        """
        result = YamlUtil.load(path)
        if not isinstance(result, list):
            raise TypeError(f"YAML文件内容不是列表类型，实际类型: {type(result).__name__}")
        return result
