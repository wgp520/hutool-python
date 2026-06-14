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
