"""AsyncFileUtil / AsyncResourceUtil 异步 IO 测试。

需要可选依赖 aiofiles；未安装时整文件通过 pytest.importorskip 跳过。

覆盖两类方法：
  1. 判断 / 元数据类：已迁移到 aiofiles.os / aiofiles.os.path 原生异步实现
     （exist / is_dir / is_file / is_symlink / is_empty / is_dir_empty /
     file_not_empty / is_modified / content_equals / last_modified_time /
     newer_than / mkdir / mkdirs / rename / mk_parent_dirs 等）。
  2. 内容读写类：已迁移到 aiofiles.open 原生异步实现
     （read_lines_str / read_line / get_total_lines / write_utf8_map /
     write_map / append_utf8_* / load_file / load_utf8 等）。

结尾的「行为一致性（与同步对照）」分组直接断言 async 结果 == sync 结果，
确保迁移是行为保持的（behavior-preserving）。
"""

import os
import time

import pytest

aiofiles = pytest.importorskip("aiofiles")

from hutool import AsyncFileUtil, AsyncResourceUtil, FileUtil  # noqa: E402


class TestAsyncFileUtil:
    # ------------------------------------------------------------------
    # 内容读写（基础）
    # ------------------------------------------------------------------

    async def test_write_read_string(self, tmp_path):
        p = tmp_path / "a.txt"
        await AsyncFileUtil.write_string(str(p), "hello 异步")
        assert await AsyncFileUtil.read_string(str(p)) == "hello 异步"

    async def test_write_read_bytes(self, tmp_path):
        p = tmp_path / "b.bin"
        await AsyncFileUtil.write_bytes(str(p), b"\x00\x01\x02")
        assert await AsyncFileUtil.read_bytes(str(p)) == b"\x00\x01\x02"

    async def test_append_string(self, tmp_path):
        p = tmp_path / "c.txt"
        await AsyncFileUtil.write_string(str(p), "a")
        await AsyncFileUtil.append_string(str(p), "b")
        assert await AsyncFileUtil.read_string(str(p)) == "ab"

    async def test_write_lines_read_lines(self, tmp_path):
        p = tmp_path / "d.txt"
        await AsyncFileUtil.write_lines(str(p), ["l1", "l2"])
        assert await AsyncFileUtil.read_utf8_lines(str(p)) == ["l1", "l2"]

    async def test_read_missing_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            await AsyncFileUtil.read_string(str(tmp_path / "nope.txt"))

    # ---- 纯计算 / 路径方法（薄壳委托同步实现，无文件系统访问） ----

    async def test_contains_invalid(self):
        assert await AsyncFileUtil.contains_invalid("a/b?c") is True
        assert await AsyncFileUtil.contains_invalid("ok.txt") is False

    async def test_check_slip(self):
        with pytest.raises(ValueError):
            await AsyncFileUtil.check_slip("../etc/passwd")
        await AsyncFileUtil.check_slip("ok/name.txt")  # 不应抛异常

    async def test_get_name_ext_prefix(self):
        assert await AsyncFileUtil.get_name("/a/b/c.txt") == "c.txt"
        assert await AsyncFileUtil.ext_name("/a/b/c.txt") == "txt"
        assert await AsyncFileUtil.get_prefix("/a/b/c.txt") == "c"

    async def test_readable_file_size(self):
        assert await AsyncFileUtil.readable_file_size(1024) == "1.0 KB"

    async def test_is_absolute(self, tmp_path):
        assert await AsyncFileUtil.is_absolute(str(tmp_path)) is True

    # ------------------------------------------------------------------
    # 判断 / 元数据类（已迁移到 aiofiles.os / aiofiles.os.path）
    # ------------------------------------------------------------------

    async def test_exist(self, tmp_path):
        p = tmp_path / "x.txt"
        p.write_text("abc")
        assert await AsyncFileUtil.exist(str(p)) is True
        assert await AsyncFileUtil.exist(str(tmp_path / "nope")) is False

    async def test_is_file(self, tmp_path):
        p = tmp_path / "x.txt"
        p.write_text("abc")
        assert await AsyncFileUtil.is_file(str(p)) is True
        assert await AsyncFileUtil.is_file(str(tmp_path)) is False

    async def test_is_dir(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        assert await AsyncFileUtil.is_dir(str(d)) is True
        assert await AsyncFileUtil.is_dir(str(tmp_path / "nope")) is False

    async def test_is_directory_alias(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        assert await AsyncFileUtil.is_directory(str(d)) is True
        f = tmp_path / "f.txt"
        f.write_text("x")
        assert await AsyncFileUtil.is_directory(str(f)) is False

    async def test_is_symlink(self, tmp_path):
        target = tmp_path / "target.txt"
        target.write_text("data")
        link = tmp_path / "link.txt"
        try:
            link.symlink_to(target)
            assert await AsyncFileUtil.is_symlink(str(link)) is True
        except OSError:
            pytest.skip("Cannot create symlink (no permission)")

    async def test_is_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        assert await AsyncFileUtil.is_empty(str(f)) is True
        nf = tmp_path / "nonempty.txt"
        nf.write_text("x")
        assert await AsyncFileUtil.is_empty(str(nf)) is False

    async def test_is_empty_dir(self, tmp_path):
        d = tmp_path / "empty_dir"
        d.mkdir()
        assert await AsyncFileUtil.is_empty(str(d)) is True
        (d / "file.txt").write_text("x")
        assert await AsyncFileUtil.is_empty(str(d)) is False

    async def test_is_empty_nonexistent(self, tmp_path):
        assert await AsyncFileUtil.is_empty(str(tmp_path / "ghost")) is True

    async def test_is_dir_empty(self, tmp_path):
        d = tmp_path / "d"
        d.mkdir()
        assert await AsyncFileUtil.is_dir_empty(str(d)) is True
        (d / "file.txt").write_text("x")
        assert await AsyncFileUtil.is_dir_empty(str(d)) is False
        # 不存在的路径视为空
        assert await AsyncFileUtil.is_dir_empty(str(tmp_path / "ghost")) is True

    async def test_file_not_empty(self, tmp_path):
        f = tmp_path / "nonempty.txt"
        f.write_text("content")
        assert await AsyncFileUtil.file_not_empty(str(f)) is True
        e = tmp_path / "empty.txt"
        e.write_text("")
        assert await AsyncFileUtil.file_not_empty(str(e)) is False

    async def test_is_modified(self, tmp_path):
        p = tmp_path / "mod.txt"
        p.write_text("data")
        assert await AsyncFileUtil.is_modified(str(p), 0) is True
        # 用一个未来的参考时间，文件不可能被修改
        future = time.time() + 1e9
        assert await AsyncFileUtil.is_modified(str(p), future) is False
        # 不存在的路径返回 False
        assert await AsyncFileUtil.is_modified(str(tmp_path / "ghost"), 0) is False

    async def test_content_equals(self, tmp_path):
        p1 = tmp_path / "c1.txt"
        p2 = tmp_path / "c2.txt"
        p1.write_text("same")
        p2.write_text("same")
        assert await AsyncFileUtil.content_equals(str(p1), str(p2)) is True
        p2.write_text("different")
        assert await AsyncFileUtil.content_equals(str(p1), str(p2)) is False
        # 非文件 / 不存在 → False
        assert await AsyncFileUtil.content_equals(str(p1), str(tmp_path / "ghost")) is False

    async def test_last_modified_time(self, tmp_path):
        p = tmp_path / "m.txt"
        p.write_text("x")
        mtime = await AsyncFileUtil.last_modified_time(str(p))
        assert mtime == FileUtil.last_modified_time(str(p))
        # 不存在时抛 FileNotFoundError
        with pytest.raises(FileNotFoundError):
            await AsyncFileUtil.last_modified_time(str(tmp_path / "ghost"))

    async def test_newer_than(self, tmp_path):
        old = tmp_path / "old.txt"
        new = tmp_path / "new.txt"
        old.write_text("old")
        time.sleep(0.01)
        new.write_text("new")
        assert await AsyncFileUtil.newer_than(str(new), str(old)) is True
        assert await AsyncFileUtil.newer_than(str(old), str(new)) is False
        # 参考文件不存在 → 视为更新
        ghost = tmp_path / "ghost.txt"
        assert await AsyncFileUtil.newer_than(str(old), str(ghost)) is True
        # 待比较文件不存在 → 视为未更新
        assert await AsyncFileUtil.newer_than(str(ghost), str(old)) is False

    async def test_size(self, tmp_path):
        p = tmp_path / "s.txt"
        p.write_text("abc")
        assert await AsyncFileUtil.size(str(p)) == 3

    async def test_copy_and_checksum(self, tmp_path):
        src = tmp_path / "s.txt"
        src.write_text("data")
        dst = tmp_path / "d.txt"
        await AsyncFileUtil.copy(str(src), str(dst))
        assert await AsyncFileUtil.exist(str(dst)) is True
        assert await AsyncFileUtil.checksum(str(src)) == await AsyncFileUtil.checksum(str(dst))

    async def test_del_file(self, tmp_path):
        p = tmp_path / "y.txt"
        p.write_text("z")
        assert await AsyncFileUtil.del_file(str(p)) is True
        assert await AsyncFileUtil.exist(str(p)) is False

    async def test_tail(self, tmp_path):
        p = tmp_path / "t.txt"
        p.write_text("\n".join(f"line{i}" for i in range(10)))
        assert await AsyncFileUtil.tail(str(p), 2) == ["line8", "line9"]

    # ------------------------------------------------------------------
    # 创建类（mkdir / mkdirs / rename / mk_parent_dirs 已迁移到 aiofiles.os）
    # ------------------------------------------------------------------

    async def test_mkdir(self, tmp_path):
        p = tmp_path / "sub"
        await AsyncFileUtil.mkdir(str(p))
        assert os.path.isdir(str(p))

    async def test_mkdirs(self, tmp_path):
        p = tmp_path / "a" / "b" / "c"
        await AsyncFileUtil.mkdirs(str(p))
        assert os.path.isdir(str(p))

    async def test_mkdirs_safely(self, tmp_path):
        p = tmp_path / "safe" / "dir"
        await AsyncFileUtil.mkdirs_safely(str(p))
        assert os.path.isdir(str(p))

    async def test_mk_parent_dirs(self, tmp_path):
        p = tmp_path / "sub" / "f.txt"
        await AsyncFileUtil.mk_parent_dirs(str(p))
        assert await AsyncFileUtil.exist(str(tmp_path / "sub")) is True

    async def test_rename(self, tmp_path):
        src = tmp_path / "old.txt"
        src.write_text("content")
        new_path = await AsyncFileUtil.rename(str(src), "new.txt")
        assert os.path.exists(str(new_path))
        assert os.path.exists(str(src)) is False
        assert new_path.name == "new.txt"

    async def test_rename_missing_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            await AsyncFileUtil.rename(str(tmp_path / "ghost.txt"), "new.txt")

    # ------------------------------------------------------------------
    # 内容读写类（已迁移到 aiofiles.open 原生异步实现）
    # ------------------------------------------------------------------

    async def test_read_lines_str(self, tmp_path):
        p = tmp_path / "lines.txt"
        p.write_text("line1\nline2\nline3")
        assert await AsyncFileUtil.read_lines_str(str(p)) == ["line1", "line2", "line3"]

    async def test_read_line(self, tmp_path):
        p = tmp_path / "rl.txt"
        p.write_text("第一行\n第二行\n第三行\n", encoding="utf-8")
        assert await AsyncFileUtil.read_line(str(p), 0) == "第一行"
        assert await AsyncFileUtil.read_line(str(p), 1) == "第二行"
        # 越界 → None
        assert await AsyncFileUtil.read_line(str(p), 999) is None
        # 负数 → None
        assert await AsyncFileUtil.read_line(str(p), -1) is None

    async def test_get_total_lines(self, tmp_path):
        # 注意：与同步实现一致，末尾换行不额外计一行
        p = tmp_path / "tl.txt"
        p.write_text("a\nb\n")
        assert await AsyncFileUtil.get_total_lines(str(p)) == 2
        p.write_text("a\nb")
        assert await AsyncFileUtil.get_total_lines(str(p)) == 2
        p.write_text("")
        assert await AsyncFileUtil.get_total_lines(str(p)) == 0
        p.write_text("single")
        assert await AsyncFileUtil.get_total_lines(str(p)) == 1

    async def test_write_utf8_map(self, tmp_path):
        p = tmp_path / "map.txt"
        data = {"name": "张三", "age": "25"}
        await AsyncFileUtil.write_utf8_map(str(p), data, "=")
        lines = await AsyncFileUtil.read_utf8_lines(str(p))
        assert lines == ["name=张三", "age=25"]

    async def test_write_map_custom_separator(self, tmp_path):
        p = tmp_path / "map2.txt"
        data = {"key": "val"}
        await AsyncFileUtil.write_map(str(p), data, ":")
        content = await AsyncFileUtil.read_utf8_string(str(p))
        assert "key:val" in content

    async def test_append_utf8_string(self, tmp_path):
        p = tmp_path / "append.txt"
        await AsyncFileUtil.write_utf8_string(str(p), "开始")
        await AsyncFileUtil.append_utf8_string(str(p), "追加")
        assert await AsyncFileUtil.read_utf8_string(str(p)) == "开始追加"

    async def test_append_utf8_lines(self, tmp_path):
        p = tmp_path / "append_lines.txt"
        await AsyncFileUtil.write_utf8_lines(str(p), ["a"])
        await AsyncFileUtil.append_utf8_lines(str(p), ["b", "c"])
        lines = await AsyncFileUtil.read_utf8_lines(str(p))
        assert lines == ["a", "b", "c"]

    async def test_load_file(self, tmp_path):
        p = tmp_path / "load.txt"
        p.write_text("a\nb\n")
        result = await AsyncFileUtil.load_file(str(p))
        assert isinstance(result, list)
        assert len(result) == 2

    async def test_load_utf8(self, tmp_path):
        p = tmp_path / "load_utf8.txt"
        p.write_text("你好\n世界\n", encoding="utf-8")
        assert await AsyncFileUtil.load_utf8(str(p)) == ["你好", "世界"]

    async def test_write_utf8_string_and_read(self, tmp_path):
        p = tmp_path / "test.txt"
        await AsyncFileUtil.write_utf8_string(str(p), "你好世界")
        assert await AsyncFileUtil.read_utf8_string(str(p)) == "你好世界"

    # ------------------------------------------------------------------
    # 行为一致性（与同步对照）：确保迁移是 behavior-preserving
    # ------------------------------------------------------------------

    async def test_parity_exist_isfile_isdir(self, tmp_path):
        f = tmp_path / "f.txt"
        f.write_text("x")
        d = tmp_path / "d"
        d.mkdir()
        ghost = str(tmp_path / "ghost")
        for path in (str(f), str(d), ghost):
            assert await AsyncFileUtil.exist(path) == FileUtil.exist(path)
            assert await AsyncFileUtil.is_file(path) == FileUtil.is_file(path)
            assert await AsyncFileUtil.is_dir(path) == FileUtil.is_dir(path)

    async def test_parity_is_empty(self, tmp_path):
        f = tmp_path / "f.txt"
        f.write_text("x")
        e = tmp_path / "e.txt"
        e.write_text("")
        d = tmp_path / "d"
        d.mkdir()
        de = tmp_path / "de"
        de.mkdir()
        (de / "x").write_text("x")
        for path in (str(f), str(e), str(d), str(de), str(tmp_path / "ghost")):
            assert await AsyncFileUtil.is_empty(path) == FileUtil.is_empty(path)

    async def test_parity_mkdir_mkdirs(self, tmp_path):
        for rel in ("m1", "a/b/c"):
            p = str(tmp_path / rel)
            await AsyncFileUtil.mkdirs(p)
            assert FileUtil.is_dir(p) is True

    async def test_parity_rename(self, tmp_path):
        # 同步 / 异步 rename 都对同一文件做原地重命名，无法在同一路径上二次调用，
        # 因此仅校验异步 rename 的产物（新路径名 + 旧路径消失）与同步实现语义一致。
        src = tmp_path / "src.txt"
        src.write_text("x")
        new = await AsyncFileUtil.rename(str(src), "dst.txt")
        assert new.name == "dst.txt"
        assert os.path.exists(str(new))
        assert os.path.exists(str(src)) is False

    async def test_parity_content_methods(self, tmp_path):
        f = tmp_path / "c.txt"
        f.write_text("line1\nline2\nline3")
        assert await AsyncFileUtil.read_lines_str(str(f)) == FileUtil.read_lines_str(str(f))
        assert await AsyncFileUtil.get_total_lines(str(f)) == FileUtil.get_total_lines(str(f))
        assert await AsyncFileUtil.read_line(str(f), 1) == FileUtil.read_line(str(f), 1)
        assert await AsyncFileUtil.load_utf8(str(f)) == FileUtil.load_utf8(str(f))

    async def test_parity_metadata(self, tmp_path):
        f = tmp_path / "m.txt"
        f.write_text("x")
        assert await AsyncFileUtil.last_modified_time(str(f)) == FileUtil.last_modified_time(str(f))
        assert await AsyncFileUtil.size(str(f)) == FileUtil.size(str(f))
        assert await AsyncFileUtil.is_modified(str(f), 0) == FileUtil.is_modified(str(f), 0)
        assert await AsyncFileUtil.file_not_empty(str(f)) == FileUtil.file_not_empty(str(f))


class TestAsyncResourceUtil:
    async def test_get_resource_str(self, tmp_path):
        p = tmp_path / "res.txt"
        p.write_text("resource-data", encoding="utf-8")
        content = await AsyncResourceUtil.get_resource_str(str(p))
        assert content == "resource-data"

    async def test_get_resource_bytes(self, tmp_path):
        p = tmp_path / "res.bin"
        p.write_bytes(b"\xaa\xbb")
        data = await AsyncResourceUtil.get_resource_bytes(str(p))
        assert data == b"\xaa\xbb"

    async def test_add_resource_path_and_get_resources(self, tmp_path):
        (tmp_path / "z.txt").write_text("z")
        # add_resource_path 为异步方法，注册到共享资源搜索路径
        await AsyncResourceUtil.add_resource_path(str(tmp_path))
        res = await AsyncResourceUtil.get_resources("z.txt")
        assert any(r.endswith("z.txt") for r in res)
