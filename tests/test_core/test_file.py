import os
import tempfile

import pytest

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

    # ===== 读写操作 =====

    def test_write_utf8_string_and_read(self, tmp_path):
        p = tmp_path / "test.txt"
        FileUtil.write_utf8_string(str(p), "你好世界")
        assert FileUtil.read_utf8_string(str(p)) == "你好世界"

    def test_write_utf8_lines(self, tmp_path):
        p = tmp_path / "lines.txt"
        FileUtil.write_utf8_lines(str(p), ["第一行", "第二行", "第三行"])
        lines = FileUtil.read_utf8_lines(str(p))
        assert lines == ["第一行", "第二行", "第三行"]

    def test_write_utf8_map(self, tmp_path):
        p = tmp_path / "map.txt"
        data = {"name": "张三", "age": "25"}
        FileUtil.write_utf8_map(str(p), data, "=")
        content = FileUtil.read_utf8_string(str(p))
        assert "name=张三" in content
        assert "age=25" in content

    def test_write_map_custom_separator(self, tmp_path):
        p = tmp_path / "map2.txt"
        data = {"key": "val"}
        FileUtil.write_map(str(p), data, ":")
        content = FileUtil.read_utf8_string(str(p))
        assert "key:val" in content

    def test_append_utf8_string(self, tmp_path):
        p = tmp_path / "append.txt"
        FileUtil.write_utf8_string(str(p), "开始")
        FileUtil.append_utf8_string(str(p), "追加")
        assert FileUtil.read_utf8_string(str(p)) == "开始追加"

    def test_append_utf8_lines(self, tmp_path):
        p = tmp_path / "append_lines.txt"
        FileUtil.write_utf8_lines(str(p), ["a"])
        FileUtil.append_utf8_lines(str(p), ["b", "c"])
        lines = FileUtil.read_utf8_lines(str(p))
        assert lines == ["a", "b", "c"]

    def test_read_utf8_string(self, tmp_path):
        p = tmp_path / "read_utf8.txt"
        p.write_text("测试内容", encoding="utf-8")
        assert FileUtil.read_utf8_string(str(p)) == "测试内容"

    def test_read_line(self, tmp_path):
        p = tmp_path / "readline.txt"
        p.write_text("第一行\n第二行\n第三行\n", encoding="utf-8")
        assert FileUtil.read_line(str(p), 0) == "第一行"
        assert FileUtil.read_line(str(p), 1) == "第二行"

    def test_read_line_out_of_range(self, tmp_path):
        p = tmp_path / "readline2.txt"
        p.write_text("only\n", encoding="utf-8")
        assert FileUtil.read_line(str(p), 999) is None

    def test_load_file(self, tmp_path):
        p = tmp_path / "load.txt"
        p.write_text("line1\nline2\n", encoding="utf-8")
        result = FileUtil.load_file(str(p))
        assert isinstance(result, list)
        assert len(result) == 2

    def test_load_utf8(self, tmp_path):
        p = tmp_path / "load_utf8.txt"
        p.write_text("你好\n世界\n", encoding="utf-8")
        result = FileUtil.load_utf8(str(p))
        assert result == ["你好", "世界"]

    # ===== 路径操作 =====

    def test_get_absolute_path(self, tmp_path):
        p = tmp_path / "test.txt"
        p.touch()
        abs_path = FileUtil.get_absolute_path(str(p))
        assert os.path.isabs(abs_path)

    def test_get_canonical_path(self, tmp_path):
        p = tmp_path / "test.txt"
        p.touch()
        canon = FileUtil.get_canonical_path(str(p))
        assert ".." not in canon

    def test_get_parent(self, tmp_path):
        p = tmp_path / "a" / "b" / "c.txt"
        result = FileUtil.get_parent(str(p), 1)
        assert result.endswith("b")

    def test_get_parent_depth(self, tmp_path):
        p = tmp_path / "a" / "b" / "c.txt"
        result = FileUtil.get_parent(str(p), 2)
        assert result.endswith("a")

    def test_get_type(self, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("hello", encoding="utf-8")
        ftype = FileUtil.get_type(str(p))
        # txt 文件可能返回空或 "txt"
        assert isinstance(ftype, str)

    def test_get_mime_type(self, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("hello", encoding="utf-8")
        mime = FileUtil.get_mime_type(str(p))
        assert mime == "text/plain"

    def test_get_mime_type_html(self, tmp_path):
        p = tmp_path / "test.html"
        p.write_text("<html></html>", encoding="utf-8")
        mime = FileUtil.get_mime_type(str(p))
        assert mime == "text/html"

    def test_is_absolute_path(self):
        # Windows 上 /tmp/test 不是绝对路径
        assert FileUtil.is_absolute_path(os.path.abspath(".")) is True
        assert FileUtil.is_absolute_path("relative/path") is False

    def test_last_index_of_separator(self):
        idx = FileUtil.last_index_of_separator("/a/b/c.txt")
        assert idx > 0
        assert FileUtil.last_index_of_separator("no_sep") == -1

    def test_path_ends_with(self):
        assert FileUtil.path_ends_with("/a/b.txt", ".txt") is True
        assert FileUtil.path_ends_with("/a/b.txt", ".log") is False

    # ===== 状态检查 =====

    def test_is_dir_empty(self, tmp_path):
        d = tmp_path / "empty_dir"
        d.mkdir()
        assert FileUtil.is_dir_empty(str(d)) is True
        (d / "file.txt").touch()
        assert FileUtil.is_dir_empty(str(d)) is False

    def test_is_directory(self, tmp_path):
        d = tmp_path / "dir"
        d.mkdir()
        assert FileUtil.is_directory(str(d)) is True
        p = tmp_path / "file.txt"
        p.touch()
        assert FileUtil.is_directory(str(p)) is False

    def test_is_modified(self, tmp_path):
        p = tmp_path / "mod.txt"
        p.write_text("data", encoding="utf-8")
        # 文件修改时间 > 0 应该返回 True
        assert FileUtil.is_modified(str(p), 0) is True

    def test_file_not_empty(self, tmp_path):
        p = tmp_path / "nonempty.txt"
        p.write_text("content", encoding="utf-8")
        assert FileUtil.file_not_empty(str(p)) is True
        e = tmp_path / "empty.txt"
        e.write_text("", encoding="utf-8")
        assert FileUtil.file_not_empty(str(e)) is False

    def test_is_sub_path(self, tmp_path):
        parent = str(tmp_path)
        child = str(tmp_path / "sub" / "file.txt")
        assert FileUtil.is_sub_path(parent, child) is True
        assert FileUtil.is_sub_path(child, parent) is False

    def test_path_equals(self, tmp_path):
        p1 = tmp_path / "a.txt"
        p1.touch()
        assert FileUtil.path_equals(str(p1), str(p1)) is True

    def test_content_equals(self, tmp_path):
        p1 = tmp_path / "c1.txt"
        p2 = tmp_path / "c2.txt"
        p1.write_text("same", encoding="utf-8")
        p2.write_text("same", encoding="utf-8")
        assert FileUtil.content_equals(str(p1), str(p2)) is True
        p2.write_text("different", encoding="utf-8")
        assert FileUtil.content_equals(str(p1), str(p2)) is False

    # ===== 创建操作 =====

    def test_mk_parent_dirs(self, tmp_path):
        p = tmp_path / "a" / "b" / "c" / "file.txt"
        FileUtil.mk_parent_dirs(str(p))
        assert p.parent.exists()

    def test_mkdirs_safely(self, tmp_path):
        d = tmp_path / "safe" / "dir"
        FileUtil.mkdirs_safely(str(d))
        assert d.exists()

    def test_new_file(self, tmp_path):
        p = tmp_path / "new.txt"
        FileUtil.new_file(str(p))
        assert p.exists()

    def test_readable_file_size(self):
        assert FileUtil.readable_file_size(1024) == "1.0 KB"
        assert FileUtil.readable_file_size(1048576) == "1.0 MB"
        assert FileUtil.readable_file_size(500) == "500 B"

    # ===== 内容操作 =====

    def test_copy_content(self, tmp_path):
        src = tmp_path / "src.txt"
        dest = tmp_path / "dest.txt"
        src.write_text("copy me", encoding="utf-8")
        FileUtil.copy_content(str(src), str(dest))
        assert dest.read_text(encoding="utf-8") == "copy me"

    def test_copy_content_no_override(self, tmp_path):
        src = tmp_path / "src2.txt"
        dest = tmp_path / "dest2.txt"
        src.write_text("new", encoding="utf-8")
        dest.write_text("old", encoding="utf-8")
        FileUtil.copy_content(str(src), str(dest), is_override=False)
        assert dest.read_text(encoding="utf-8") == "old"

    def test_move_content(self, tmp_path):
        src = tmp_path / "move_src.txt"
        dest = tmp_path / "move_dest.txt"
        src.write_text("move me", encoding="utf-8")
        FileUtil.move_content(str(src), str(dest))
        assert not src.exists()
        assert dest.read_text(encoding="utf-8") == "move me"

    def test_convert_charset(self, tmp_path):
        p = tmp_path / "charset.txt"
        p.write_bytes("你好".encode())
        FileUtil.convert_charset(str(p), "utf-8", "gbk")
        content = p.read_bytes().decode("gbk")
        assert content == "你好"

    def test_convert_line_separator(self, tmp_path):
        p = tmp_path / "linesep.txt"
        p.write_bytes(b"a\r\nb\r\nc\r\n")
        FileUtil.convert_line_separator(str(p), "\n")
        content = p.read_bytes()
        assert b"\r\n" not in content
        assert content == b"a\nb\nc\n"

    def test_copy_files_from_dir(self, tmp_path):
        src = tmp_path / "src_dir"
        dest = tmp_path / "dest_dir"
        src.mkdir()
        (src / "a.txt").write_text("a", encoding="utf-8")
        (src / "b.txt").write_text("b", encoding="utf-8")
        dest.mkdir()
        FileUtil.copy_files_from_dir(str(src), str(dest))
        assert (dest / "a.txt").exists()
        assert (dest / "b.txt").exists()

    def test_check_slip(self, tmp_path):
        # 正常路径不抛异常
        FileUtil.check_slip(str(tmp_path / "safe.txt"))
        FileUtil.check_slip("a/b/c.txt")
        # 路径穿越应抛 ValueError
        with pytest.raises(ValueError):
            FileUtil.check_slip("a/../../etc/passwd")
        with pytest.raises(ValueError):
            FileUtil.check_slip("../secret.txt")

    def test_checksum(self, tmp_path):
        p = tmp_path / "ck.txt"
        p.write_text("hello", encoding="utf-8")
        md5 = FileUtil.checksum(str(p), "md5")
        assert isinstance(md5, str)
        assert len(md5) == 32  # MD5 hex length

    def test_checksum_sha256(self, tmp_path):
        import hashlib

        p = tmp_path / "ck2.txt"
        p.write_text("test", encoding="utf-8")
        expected = hashlib.sha256(b"test").hexdigest()
        assert FileUtil.checksum(str(p), "sha256") == expected

    def test_checksum_crc32(self, tmp_path):
        p = tmp_path / "crc.txt"
        p.write_text("hello", encoding="utf-8")
        crc = FileUtil.checksum_crc32(str(p))
        assert isinstance(crc, int)
        assert crc != 0

    # ===== 清理操作 =====

    def test_clean_empty(self, tmp_path):
        d = tmp_path / "clean_test"
        d.mkdir()
        empty_file = d / "empty.txt"
        empty_file.write_text("", encoding="utf-8")
        empty_dir = d / "empty_sub"
        empty_dir.mkdir()
        count = FileUtil.clean_empty(str(d))
        assert count >= 2
        assert not empty_file.exists()
        assert not empty_dir.exists()

    def test_clean_invalid(self, tmp_path):
        d = tmp_path / "invalid_test"
        d.mkdir()
        # 无效文件名在 Windows 上无法创建，跳过该部分
        valid = d / "valid.txt"
        valid.write_text("ok", encoding="utf-8")
        count = FileUtil.clean_invalid(str(d))
        assert isinstance(count, int)

    def test_contains_invalid(self):
        assert FileUtil.contains_invalid("valid_name.txt") is False
        assert FileUtil.contains_invalid("file\x00name") is True

    # ===== is_symlink =====

    def test_is_symlink(self, tmp_path):
        target = tmp_path / "target.txt"
        target.write_text("data", encoding="utf-8")
        link = tmp_path / "link.txt"
        try:
            link.symlink_to(target)
            assert FileUtil.is_symlink(str(link)) is True
        except OSError:
            # Windows 可能需要特殊权限创建 symlink，跳过
            pytest.skip("Cannot create symlink (no permission)")

    # ===== tail =====

    def test_tail_with_handler(self, tmp_path):
        p = tmp_path / "handler.txt"
        lines = [f"line{i}" for i in range(20)]
        p.write_text("\n".join(lines), encoding="utf-8")
        collected = []
        result = FileUtil.tail(str(p), 3, handler=lambda x: collected.append(x))
        assert len(result) == 3
        assert len(collected) == 3
        assert collected == result

    def test_tail_with_charset(self, tmp_path):
        p = tmp_path / "charset_tail.txt"
        p.write_bytes("中文\n内容\n".encode())
        result = FileUtil.tail(str(p), 2, charset="utf-8")
        assert len(result) == 2
