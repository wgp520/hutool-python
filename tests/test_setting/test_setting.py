import io
import os
import tempfile

import pytest

from hutool import PropsUtil, SettingUtil, YamlUtil


class TestYamlUtil:
    def test_load_by_string(self):
        yaml_str = """
database:
  host: localhost
  port: 3306
  name: test_db
"""
        result = YamlUtil.load_by_string(yaml_str)
        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 3306

    def test_load(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            f.write("key: value\nlist:\n  - a\n  - b\n")
            path = f.name
        try:
            result = YamlUtil.load(path)
            assert result["key"] == "value"
            assert result["list"] == ["a", "b"]
        finally:
            os.unlink(path)

    def test_dump(self):
        data = {"key": "value", "nested": {"a": 1}}
        result = YamlUtil.dump(data)
        assert "key" in result
        assert "value" in result

    def test_dump_to_file(self):
        data = {"key": "value"}
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.yaml")
            YamlUtil.dump(data, path=path)
            assert os.path.exists(path)
            result = YamlUtil.load(path)
            assert result["key"] == "value"

    def test_load_as_dict(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml", encoding="utf-8") as f:
            f.write("key: value\nname: test\n")
            path = f.name
        try:
            result = YamlUtil.load_as_dict(path)
            assert isinstance(result, dict)
            assert result["key"] == "value"
        finally:
            os.unlink(path)

    def test_load_as_list(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml", encoding="utf-8") as f:
            f.write("- a\n- b\n- c\n")
            path = f.name
        try:
            result = YamlUtil.load_as_list(path)
            assert isinstance(result, list)
            assert result == ["a", "b", "c"]
        finally:
            os.unlink(path)

    def test_dump_to(self):
        buf = io.StringIO()
        YamlUtil.dump_to({"key": "value"}, buf)
        content = buf.getvalue()
        assert "key" in content
        assert "value" in content


class TestPropsUtil:
    def test_load(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".properties", delete=False, encoding="utf-8") as f:
            f.write("key1=value1\nkey2=value2\n# comment\nkey3=value3\n")
            path = f.name
        try:
            result = PropsUtil.load(path)
            assert result["key1"] == "value1"
            assert result["key2"] == "value2"
            assert result["key3"] == "value3"
        finally:
            os.unlink(path)

    def test_get(self):
        props = {"key": "value", "num": "42"}
        assert PropsUtil.get(props, "key") == "value"
        assert PropsUtil.get(props, "num") == "42"
        assert PropsUtil.get(props, "missing", "default") == "default"
        assert PropsUtil.get(props, "missing") is None

    def test_load_with_spaces(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".properties", delete=False, encoding="utf-8") as f:
            f.write("key1 = value1\n  key2  =  value2  \n")
            path = f.name
        try:
            result = PropsUtil.load(path)
            assert result["key1"] == "value1"
            assert result["key2"] == "value2"
        finally:
            os.unlink(path)

    def test_load_nonexistent(self):
        with pytest.raises(FileNotFoundError):
            PropsUtil.load("/nonexistent/path.properties")

    def test_create(self):
        p = PropsUtil.create()
        assert isinstance(p, dict)

    def test_store(self):
        p = {"key": "value", "num": "123"}
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".properties", encoding="utf-8") as f:
            path = f.name
        try:
            PropsUtil.store(p, path, comment="Test")
            assert os.path.getsize(path) > 0
            loaded = PropsUtil.load(path)
            assert loaded["key"] == "value"
        finally:
            os.unlink(path)

    def test_to_dict(self):
        p = {"a": 1}
        d = PropsUtil.to_dict(p)
        assert d == p


class TestSettingUtil:
    def test_create(self):
        s = SettingUtil.create()
        assert isinstance(s, dict)
        assert len(s) == 0

    def test_set_value(self):
        s = {}
        SettingUtil.set_value(s, "key", "value")
        assert s["key"] == "value"

    def test_to_dict(self):
        s = {"a": 1, "b": 2}
        d = SettingUtil.to_dict(s)
        assert d == s
        assert d is not s  # different object

    def test_get_group(self):
        s = {"db.host": "localhost", "db.port": 3306, "app.name": "test"}
        group = SettingUtil.get_group(s, "db.")
        assert len(group) == 2
        assert "host" in group or "db.host" in group

    def test_store(self):
        s = {"key1": "value1", "key2": 42}
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".properties", encoding="utf-8") as f:
            path = f.name
        try:
            SettingUtil.store(s, path, comment="Test config")
            assert os.path.getsize(path) > 0
            loaded = SettingUtil.load(path)
            assert loaded["key1"] == "value1"
        finally:
            os.unlink(path)
