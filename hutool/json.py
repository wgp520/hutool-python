import json
import re
import xml.etree.ElementTree as ET
from typing import Any, Callable, Dict, List, Optional, Type, Union


def _element_to_dict(element: ET.Element):
    """递归将 XML Element 转为字典。

    :param element: XML 元素
    :return: 转换后的字典或字符串
    """
    result = {}
    if element.text and element.text.strip():
        if len(element) == 0:
            return element.text.strip()
        result["#text"] = element.text.strip()
    for child in element:
        child_data = _element_to_dict(child)
        if child.tag in result:
            existing = result[child.tag]
            if not isinstance(existing, list):
                result[child.tag] = [existing]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    if element.attrib:
        for key, val in element.attrib.items():
            result[f"@{key}"] = val
    return result


class JSONUtil:
    """JSON工具类，提供 JSON 的解析、序列化、校验、路径操作等功能。"""

    @staticmethod
    def create_obj() -> dict:
        """
        创建空JSON对象。

        :return: 空字典
        """
        return {}

    @staticmethod
    def create_array() -> list:
        """
        创建空JSON数组。

        :return: 空列表
        """
        return []

    # ------------------------------------------------------------------ #
    #  解析
    # ------------------------------------------------------------------ #

    @staticmethod
    def parse_obj(json_str: str) -> dict:
        """
        解析JSON字符串为字典。

        :param json_str: JSON字符串
        :return: 字典
        :raises ValueError: JSON字符串不是对象类型时
        """
        result = json.loads(json_str)
        if not isinstance(result, dict):
            raise ValueError("JSON字符串不是对象类型")
        return result

    @staticmethod
    def parse_array(json_str: str) -> list:
        """
        解析JSON字符串为列表。

        :param json_str: JSON字符串
        :return: 列表
        :raises ValueError: JSON字符串不是数组类型时
        """
        result = json.loads(json_str)
        if not isinstance(result, list):
            raise ValueError("JSON字符串不是数组类型")
        return result

    @staticmethod
    def parse(json_str: str):
        """
        解析JSON字符串，自动返回对应Python类型。

        :param json_str: JSON字符串
        :return: 解析后的Python对象
        """
        return json.loads(json_str)

    # ------------------------------------------------------------------ #
    #  序列化
    # ------------------------------------------------------------------ #

    @staticmethod
    def to_json_str(obj: Any, indent: Optional[int] = None) -> str:
        """
        对象转JSON字符串。

        :param obj: 待序列化的对象
        :param indent: 缩进空格数，None表示不缩进
        :return: JSON字符串
        """
        return json.dumps(obj, ensure_ascii=False, indent=indent)

    @staticmethod
    def to_json_pretty_str(obj: Any) -> str:
        """
        对象转格式化JSON字符串（缩进2空格）。

        :param obj: 待序列化的对象
        :return: 格式化的JSON字符串
        """
        return json.dumps(obj, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------ #
    #  Bean 转换（简易实现，基于类构造器）
    # ------------------------------------------------------------------ #

    @staticmethod
    def to_bean(json_str: str, bean_class: Type):
        """
        JSON字符串转对象。

        将JSON解析为字典后，通过 ``bean_class(**dict)`` 构造实例。
        如果 bean_class 提供了 ``from_dict`` 类方法，则优先调用。

        :param json_str: JSON字符串
        :param bean_class: 目标类型
        :return: 目标类型的实例
        """
        data = json.loads(json_str)
        if hasattr(bean_class, "from_dict") and callable(bean_class.from_dict):
            return bean_class.from_dict(data)
        if isinstance(data, dict):
            return bean_class(**data)
        return bean_class(data)

    @staticmethod
    def to_bean_list(json_str: str, element_class: Type) -> list:
        """
        JSON字符串转对象列表。

        :param json_str: JSON字符串（数组格式）
        :param element_class: 元素目标类型
        :return: 对象列表
        :raises ValueError: JSON字符串不是数组类型时
        """
        data = json.loads(json_str)
        if not isinstance(data, list):
            raise ValueError("JSON字符串不是数组类型")
        if hasattr(element_class, "from_dict") and callable(element_class.from_dict):
            return [element_class.from_dict(item) for item in data]
        return [element_class(**item) if isinstance(item, dict) else element_class(item) for item in data]

    @staticmethod
    def from_bean(obj: Any) -> str:
        """
        对象转JSON字符串。

        如果对象具有 ``to_dict`` 方法则先调用，否则直接序列化。

        :param obj: 待序列化的对象
        :return: JSON字符串
        """
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return json.dumps(obj.to_dict(), ensure_ascii=False)
        return json.dumps(obj, ensure_ascii=False, default=str)

    # ------------------------------------------------------------------ #
    #  文件读写
    # ------------------------------------------------------------------ #

    @staticmethod
    def read_json(path: str, charset: str = "utf-8"):
        """
        读取JSON文件并解析。

        :param path: 文件路径
        :param charset: 文件编码
        :return: 解析后的Python对象
        """
        with open(path, encoding=charset) as f:
            return json.load(f)

    @staticmethod
    def read_json_object(path: str, charset: str = "utf-8") -> dict:
        """
        读取JSON文件为字典。

        :param path: 文件路径
        :param charset: 文件编码
        :return: 字典
        :raises ValueError: JSON文件内容不是对象类型时
        """
        result = JSONUtil.read_json(path, charset)
        if not isinstance(result, dict):
            raise ValueError("JSON文件内容不是对象类型")
        return result

    @staticmethod
    def read_json_array(path: str, charset: str = "utf-8") -> list:
        """
        读取JSON文件为列表。

        :param path: 文件路径
        :param charset: 文件编码
        :return: 列表
        :raises ValueError: JSON文件内容不是数组类型时
        """
        result = JSONUtil.read_json(path, charset)
        if not isinstance(result, list):
            raise ValueError("JSON文件内容不是数组类型")
        return result

    @staticmethod
    def write_json(path: str, obj: Any, charset: str = "utf-8", indent: Optional[int] = None) -> None:
        """
        写入JSON文件。

        :param path: 文件路径
        :param obj: 待写入对象
        :param charset: 文件编码
        :param indent: 缩进空格数，None表示不缩进
        """
        with open(path, "w", encoding=charset) as f:
            json.dump(obj, f, ensure_ascii=False, indent=indent)

    # ------------------------------------------------------------------ #
    #  校验
    # ------------------------------------------------------------------ #

    @staticmethod
    def is_json(str_val: str) -> bool:
        """
        是否为有效JSON。

        :param str_val: 待检查的字符串
        :return: 是否为有效JSON
        """
        if not str_val or not isinstance(str_val, str):
            return False
        str_val = str_val.strip()
        if not str_val:
            return False
        try:
            json.loads(str_val)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_json_obj(str_val: str) -> bool:
        """
        是否为JSON对象。

        :param str_val: 待检查的字符串
        :return: 是否为JSON对象
        """
        if not str_val or not isinstance(str_val, str):
            return False
        str_val = str_val.strip()
        if not str_val:
            return False
        try:
            return isinstance(json.loads(str_val), dict)
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_json_array(str_val: str) -> bool:
        """
        是否为JSON数组。

        :param str_val: 待检查的字符串
        :return: 是否为JSON数组
        """
        if not str_val or not isinstance(str_val, str):
            return False
        str_val = str_val.strip()
        if not str_val:
            return False
        try:
            return isinstance(json.loads(str_val), list)
        except (json.JSONDecodeError, TypeError):
            return False

    # ------------------------------------------------------------------ #
    #  格式化 / 压缩
    # ------------------------------------------------------------------ #

    @staticmethod
    def format_json(json_str: str, indent: int = 2) -> str:
        """
        格式化JSON字符串。

        :param json_str: JSON字符串
        :param indent: 缩进空格数
        :return: 格式化后的JSON字符串
        """
        obj = json.loads(json_str)
        return json.dumps(obj, ensure_ascii=False, indent=indent)

    @staticmethod
    def compress(json_str: str) -> str:
        """
        压缩JSON（去除所有空白）。

        :param json_str: JSON字符串
        :return: 压缩后的JSON字符串
        """
        obj = json.loads(json_str)
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

    # ------------------------------------------------------------------ #
    #  路径操作（支持 'a.b.c' 和 'a[0].b'）
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_path_keys(path: str) -> List[Union[str, int]]:
        """
        将路径字符串解析为键列表。

        例如 ``'a.b[0].c'`` 解析为 ``['a', 'b', 0, 'c']``

        :param path: 路径字符串
        :return: 键列表
        """
        keys: List[Union[str, int]] = []
        for part in re.split(r"\.(?![^\[]*\])", path):
            # 处理 key[index] 形式
            match = re.match(r"^(\w+)((?:\[\d+\])*)$", part)
            if match:
                keys.append(match.group(1))
                for idx in re.findall(r"\[(\d+)\]", match.group(2)):
                    keys.append(int(idx))
            elif part:
                keys.append(part)
        return keys

    @staticmethod
    def get_by_path(json_data: Any, path: str) -> Any:
        """按路径获取值

        :param json_data: JSON数据（字典或列表）
        :param path: 路径，如 'a.b.c' 或 'a[0].b'
        :return: 对应路径的值，路径不存在时返回 None
        """
        keys = JSONUtil._parse_path_keys(path)
        current = json_data
        for key in keys:
            if current is None:
                return None
            try:
                current = current[key]
            except (KeyError, IndexError, TypeError):
                return None
        return current

    @staticmethod
    def put_by_path(json_data: Any, path: str, value: Any) -> None:
        """按路径设置值

        :param json_data: JSON数据（字典或列表）
        :param path: 路径，如 'a.b.c' 或 'a[0].b'
        :param value: 要设置的值
        """
        keys = JSONUtil._parse_path_keys(path)
        if not keys:
            raise ValueError("路径不能为空")
        current = json_data
        for key in keys[:-1]:
            next_key = keys[keys.index(key) + 1] if keys.index(key) + 1 < len(keys) else None
            if isinstance(current, dict):
                if key not in current:
                    current[key] = {} if isinstance(next_key, str) else []
                current = current[key]
            elif isinstance(current, list):
                while len(current) <= key:
                    current.append(None)
                if current[key] is None:
                    current[key] = {} if isinstance(next_key, str) else []
                current = current[key]
            else:
                raise TypeError(f"无法在路径 '{path}' 上设置值：中间节点类型不支持")
        last_key = keys[-1]
        current[last_key] = value

    # ------------------------------------------------------------------ #
    #  键名映射
    # ------------------------------------------------------------------ #

    @staticmethod
    def map_dict_keys(func: Callable, obj: Any) -> Any:
        """
        递归映射 JSON 对象（字典）的所有键名。

        对嵌套的字典和列表递归处理。

        Examples::

            map_dict_keys(str.upper, {"a": 1, "b": {"c": 2}})
            -> {"A": 1, "B": {"C": 2}}

        :param func: 键名映射函数
        :param obj: JSON 对象（字典）或列表
        :return: 映射后的新对象
        """
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                func_key = func(key)
                if isinstance(value, dict):
                    new_obj[func_key] = JSONUtil.map_dict_keys(func, value)
                elif isinstance(value, list):
                    new_obj[func_key] = JSONUtil.map_list_keys(func, value)
                else:
                    new_obj[func_key] = value
            return new_obj
        return obj

    @staticmethod
    def map_list_keys(func: Callable, lst: list) -> list:
        """
        递归映射列表中所有字典的键名。

        :param func: 键名映射函数
        :param lst: 列表
        :return: 映射后的新列表
        """
        result = []
        for item in lst:
            if isinstance(item, dict):
                result.append(JSONUtil.map_dict_keys(func, item))
            else:
                result.append(item)
        return result

    @staticmethod
    def convert_keys_to_camel(obj: Dict) -> Dict:
        """
        将 JSON 对象的所有键名从 ``snake_case`` 转为 ``camelCase``。

        Examples::

            convert_keys_to_camel({"user_name": "Tom", "home_addr": {"zip_code": "100000"}})
            -> {"userName": "Tom", "homeAddr": {"zipCode": "100000"}}

        :param obj: 字典对象
        :return: 键名转换后的新字典
        """

        def _to_camel(key: str) -> str:
            parts = key.split("_")
            return parts[0] + "".join(p.title() for p in parts[1:])

        return JSONUtil.map_dict_keys(_to_camel, obj)

    @staticmethod
    def convert_keys_to_snake(obj: Dict) -> Dict:
        """
        将 JSON 对象的所有键名从 ``camelCase`` 转为 ``snake_case``。

        Examples::

            convert_keys_to_snake({"userName": "Tom", "homeAddr": {"zipCode": "100000"}})
            -> {"user_name": "Tom", "home_addr": {"zip_code": "100000"}}

        :param obj: 字典对象
        :return: 键名转换后的新字典
        """
        _camel_pattern = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

        def _to_snake(key: str) -> str:
            return _camel_pattern.sub("_", key).lower()

        return JSONUtil.map_dict_keys(_to_snake, obj)

    # ------------------------------------------------------------------ #
    #  转义 / 引号
    # ------------------------------------------------------------------ #

    @staticmethod
    def quote(s: str) -> str:
        """用双引号包裹字符串并进行JSON转义

        :param s: 原始字符串
        :return: JSON引号包裹的字符串
        """
        return json.dumps(s)

    @staticmethod
    def escape(s: str) -> str:
        """JSON字符串转义

        将特殊字符转为JSON转义序列。

        :param s: 原始字符串
        :return: 转义后的字符串
        """
        result = []
        for ch in s:
            if ch == '"':
                result.append('\\"')
            elif ch == "\\":
                result.append("\\\\")
            elif ch == "\b":
                result.append("\\b")
            elif ch == "\f":
                result.append("\\f")
            elif ch == "\n":
                result.append("\\n")
            elif ch == "\r":
                result.append("\\r")
            elif ch == "\t":
                result.append("\\t")
            elif ord(ch) < 0x20:
                result.append(f"\\u{ord(ch):04x}")
            else:
                result.append(ch)
        return "".join(result)

    # ------------------------------------------------------------------ #
    #  判空
    # ------------------------------------------------------------------ #

    @staticmethod
    def is_null(json_str: str) -> bool:
        """判断JSON字符串是否为null

        :param json_str: JSON字符串
        :return: 是否为null
        """
        if json_str is None:
            return True
        stripped = json_str.strip()
        return stripped == "null" or stripped == ""

    # ------------------------------------------------------------------ #
    #  XML 转换
    # ------------------------------------------------------------------ #

    @staticmethod
    def xml_to_json(xml_str: str) -> dict:
        """XML字符串转JSON字典

        简单的XML到字典转换。

        :param xml_str: XML字符串
        :return: 转换后的字典
        """

        def _element_to_dict(element):
            # type: (ET.Element) -> dict
            result = {}
            # 处理属性
            if element.attrib:
                for k, v in element.attrib.items():
                    result[f"@{k}"] = v
            # 处理子元素
            children = list(element)
            if children:
                child_map = {}
                for child in children:
                    child_dict = _element_to_dict(child)
                    tag = child.tag
                    if tag in child_map:
                        if not isinstance(child_map[tag], list):
                            child_map[tag] = [child_map[tag]]
                        child_map[tag].append(child_dict)
                    else:
                        child_map[tag] = child_dict
                result.update(child_map)
            # 处理文本
            if element.text and element.text.strip():
                if result:
                    result["#text"] = element.text.strip()
                else:
                    return element.text.strip()
            return result

        root = ET.fromstring(xml_str)
        return {root.tag: _element_to_dict(root)}

    # ------------------------------------------------------------------ #
    #  字节序列化
    # ------------------------------------------------------------------ #

    @staticmethod
    def to_json_bytes(obj: Any, charset: str = "utf-8") -> bytes:
        """对象转JSON字节数组

        :param obj: 待序列化对象
        :param charset: 字符集
        :return: JSON字节数组
        """
        return json.dumps(obj, ensure_ascii=False).encode(charset)

    # ------------------------------------------------------------------ #
    #  便捷方法
    # ------------------------------------------------------------------ #

    @staticmethod
    def wrap(obj: Any) -> str:
        """将对象包装为JSON字符串（to_json_str别名）

        :param obj: 对象
        :return: JSON字符串
        """
        return JSONUtil.to_json_str(obj)

    @staticmethod
    def get_str(json_data: dict, key: str, default: str = "") -> str:
        """从JSON对象获取字符串值

        :param json_data: JSON字典
        :param key: 键名
        :param default: 默认值
        :return: 字符串值
        """
        value = json_data.get(key, default)
        if value is None:
            return default
        return str(value)

    @staticmethod
    def get_int(json_data: dict, key: str, default: int = 0) -> int:
        """从JSON对象获取整数值

        :param json_data: JSON字典
        :param key: 键名
        :param default: 默认值
        :return: 整数值
        """
        value = json_data.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def get_float(json_data: dict, key: str, default: float = 0.0) -> float:
        """从JSON对象获取浮点值

        :param json_data: JSON字典
        :param key: 键名
        :param default: 默认值
        :return: 浮点值
        """
        value = json_data.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def get_bool(json_data: dict, key: str, default: bool = False) -> bool:
        """从JSON对象获取布尔值

        :param json_data: JSON字典
        :param key: 键名
        :param default: 默认值
        :return: 布尔值
        """
        value = json_data.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return bool(value)

    @staticmethod
    def get_list(json_data: dict, key: str, default: Optional[list] = None) -> list:
        """从JSON对象获取列表值

        :param json_data: JSON字典
        :param key: 键名
        :param default: 默认值
        :return: 列表值
        """
        if default is None:
            default = []
        value = json_data.get(key)
        if value is None:
            return default
        if isinstance(value, list):
            return value
        return default

    @staticmethod
    def parse_from_xml(xml_str: str) -> dict:
        """将 XML 字符串解析为字典。

        :param xml_str: XML 字符串
        :return: 解析后的字典
        """
        root = ET.fromstring(xml_str)
        return _element_to_dict(root)

    @staticmethod
    def get_ordered_json(s: str) -> str:
        """获取排序键名后的 JSON 字符串（用于比较）。

        :param s: JSON 字符串
        :return: 排序键名后的 JSON 字符串
        """
        obj = json.loads(s)
        return json.dumps(obj, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def json_equal(s1: str, s2: str) -> bool:
        """比较两个 JSON 是否语义相等（忽略键顺序）。

        :param s1: JSON 字符串 1
        :param s2: JSON 字符串 2
        :return: 是否相等
        """
        obj1 = json.loads(s1)
        obj2 = json.loads(s2)
        return obj1 == obj2

    @staticmethod
    def json_keys_equal(s1: str, s2: str) -> bool:
        """比较两个 JSON 的键集合是否相等（仅对象类型）。

        :param s1: JSON 字符串 1
        :param s2: JSON 字符串 2
        :return: 键集合是否相等
        """
        obj1 = json.loads(s1)
        obj2 = json.loads(s2)
        if not isinstance(obj1, dict) or not isinstance(obj2, dict):
            return False
        return set(obj1.keys()) == set(obj2.keys())
