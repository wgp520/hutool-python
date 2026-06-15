import os
import tempfile

from hutool import FileUtil


class TestFileUtil:
    def test_exist(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        try:
            assert FileUtil.exist(path) is True
            assert FileUtil.exist("/nonexistent/path") is False
        finally:
            os.unlink(path)

    def test_is_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        try:
            assert FileUtil.is_file(path) is True
            assert FileUtil.is_file(os.path.dirname(path)) is False
        finally:
            os.unlink(path)

    def test_is_dir(self):
        with tempfile.TemporaryDirectory() as d:
            assert FileUtil.is_dir(d) is True
            assert FileUtil.is_dir(os.path.join(d, "nonexistent")) is False

    def test_touch(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.txt")
            FileUtil.touch(path)
            assert os.path.exists(path)

    def test_mkdir(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "subdir")
            FileUtil.mkdir(path)
            assert os.path.isdir(path)

    def test_mkdirs(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "a", "b", "c")
            FileUtil.mkdirs(path)
            assert os.path.isdir(path)

    def test_read_write_string(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.txt")
            FileUtil.write_string(path, "Hello, World!")
            result = FileUtil.read_string(path)
            assert result == "Hello, World!"

    def test_read_write_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.bin")
            FileUtil.write_bytes(path, b"\x00\x01\x02")
            result = FileUtil.read_bytes(path)
            assert result == b"\x00\x01\x02"

    def test_read_lines(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.txt")
            FileUtil.write_string(path, "line1\nline2\nline3")
            result = FileUtil.read_lines_str(path)
            assert result == ["line1", "line2", "line3"]

    def test_append_string(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.txt")
            FileUtil.write_string(path, "Hello")
            FileUtil.append_string(path, ", World!")
            result = FileUtil.read_string(path)
            assert result == "Hello, World!"

    def test_copy(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "src.txt")
            dest = os.path.join(d, "dest.txt")
            FileUtil.write_string(src, "content")
            FileUtil.copy(src, dest)
            assert FileUtil.read_string(dest) == "content"

    def test_move(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "src.txt")
            dest = os.path.join(d, "dest.txt")
            FileUtil.write_string(src, "content")
            FileUtil.move(src, dest)
            assert not os.path.exists(src)
            assert FileUtil.read_string(dest) == "content"

    def test_del(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.txt")
            FileUtil.write_string(path, "content")
            FileUtil.del_file(path)
            assert not os.path.exists(path)

    def test_get_name(self):
        assert FileUtil.get_name("/path/to/file.txt") == "file.txt"

    def test_get_suffix(self):
        assert FileUtil.get_suffix("/path/to/file.txt") == "txt"

    def test_get_prefix(self):
        assert FileUtil.get_prefix("/path/to/file.txt") == "file"

    def test_main_name(self):
        assert FileUtil.main_name("/path/to/file.txt") == "file"

    def test_size(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.txt")
            FileUtil.write_string(path, "Hello")
            size = FileUtil.size(path)
            assert size > 0

    def test_loop_files(self):
        with tempfile.TemporaryDirectory() as d:
            for i in range(3):
                FileUtil.write_string(os.path.join(d, f"file{i}.txt"), f"content{i}")
            files = FileUtil.loop_files(d)
            assert len(files) == 3

    def test_clean(self):
        with tempfile.TemporaryDirectory() as d:
            for i in range(3):
                FileUtil.write_string(os.path.join(d, f"file{i}.txt"), f"content{i}")
            FileUtil.clean(d)
            files = os.listdir(d)
            assert len(files) == 0

    def test_get_tmp_dir_path(self):
        result = FileUtil.get_tmp_dir_path()
        assert isinstance(result, str)
        assert os.path.isdir(result)

    def test_get_user_home_path(self):
        result = FileUtil.get_user_home_path()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rename(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "old.txt")
            FileUtil.write_string(path, "content")
            new_path = FileUtil.rename(path, "new.txt")
            assert os.path.exists(new_path)

    def test_sub_path(self):
        result = FileUtil.sub_path("/a/b/c.txt", 1, 3)
        assert isinstance(result, str)

    def test_write_lines(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.txt")
            FileUtil.write_lines(path, ["line1", "line2", "line3"])
            result = FileUtil.read_lines(path)
            assert len(result) == 3

    def test_newer_than(self):
        with tempfile.TemporaryDirectory() as d:
            old = os.path.join(d, "old.txt")
            new = os.path.join(d, "new.txt")
            FileUtil.write_string(old, "old")
            import time

            time.sleep(0.01)
            FileUtil.write_string(new, "new")
            assert FileUtil.newer_than(new, old) is True

    # ── tail ────────────────────────────────────────────────────────

    def test_tail_basic(self):
        """测试读取文件末尾行"""
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "tail.txt")
            lines = [f"line{i}" for i in range(100)]
            FileUtil.write_lines(path, lines)
            result = FileUtil.tail(path, 5)
            assert len(result) == 5
            assert result[0] == "line95"
            assert result[4] == "line99"

    def test_tail_fewer_lines(self):
        """测试请求行数超过文件实际行数"""
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "tail_short.txt")
            FileUtil.write_lines(path, ["a", "b", "c"])
            result = FileUtil.tail(path, 10)
            assert len(result) == 3
            assert result == ["a", "b", "c"]

    def test_tail_empty_file(self):
        """测试空文件"""
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "empty.txt")
            FileUtil.write_string(path, "")
            result = FileUtil.tail(path, 5)
            assert result == []

    def test_tail_file_not_found(self):
        """测试文件不存在"""
        import pytest

        with pytest.raises(FileNotFoundError):
            FileUtil.tail("/nonexistent/file.txt")
