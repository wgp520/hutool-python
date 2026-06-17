"""Struct 结构化数据类。

提供 dict 与 object 混合体，支持 ``obj.key`` 和 ``obj['key']`` 两种访问方式，
"""

from typing import Any

__all__ = ["Struct"]


class Struct(dict):
    """结构化字典，支持属性访问。

    ``Struct`` 继承自 ``dict``，在保留字典全部行为的同时，
    允许通过 ``obj.key`` 形式访问键值对。

    ::

        s = Struct({"name": "test", "age": 20})
        assert s.name == "test"
        assert s["age"] == 20
        s.email = "a@b.com"
        assert s["email"] == "a@b.com"
    """

    def __getattr__(self, name: str) -> Any:
        """属性访问，映射到字典键。"""
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """属性设置，映射到字典键。"""
        self[name] = value

    def __delattr__(self, name: str) -> None:
        """属性删除，映射到字典键。"""
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)

    def __repr__(self) -> str:
        items = ", ".join(f"{k}={v!r}" for k, v in self.items())
        return f"Struct({items})"

    @classmethod
    def from_dict(cls, obj: Any, recursive: bool = True) -> Any:
        """将 dict/list 递归转换为 Struct 对象。

        :param obj: 输入对象（支持 dict、list、tuple 或其他标量）
        :param recursive: 是否递归转换嵌套对象，默认 True
        :return: 转换后的对象（dict → Struct, list → 转换后的列表）

        ::

            data = {"user": {"name": "test", "tags": [{"id": 1}, {"id": 2}]}}
            s = Struct.from_dict(data)
            assert s.user.name == "test"
            assert s.user.tags[0].id == 1
        """
        if isinstance(obj, dict):
            struct = cls()
            for key, value in obj.items():
                struct[key] = cls.from_dict(value, recursive=True) if recursive else value
            return struct
        if isinstance(obj, (list, tuple)):
            converted = [cls.from_dict(item, recursive=True) if recursive else item for item in obj]
            return type(obj)(converted) if isinstance(obj, tuple) else converted
        return obj
