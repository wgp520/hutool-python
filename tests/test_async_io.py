"""AsyncFileUtil / AsyncResourceUtil 异步 IO 测试。

需要可选依赖 aiofiles；未安装时整文件通过 pytest.importorskip 跳过。
"""

import pytest

aiofiles = pytest.importorskip("aiofiles")

from hutool import AsyncFileUtil, AsyncResourceUtil  # noqa: E402


class TestAsyncFileUtil:
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
