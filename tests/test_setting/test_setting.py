import os
import tempfile

import pytest

from hutool import PropsUtil
from hutool import YamlUtil


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
