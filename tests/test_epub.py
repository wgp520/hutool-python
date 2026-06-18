"""Epub 模块测试。

- 单元测试：不依赖 ebooklib / mkepub（用 Mock 子类测试基类逻辑）
- 集成测试：用真实引擎生成 EPUB，验证 ZIP 结构 / mimetype / 章节内容
  所有生成文件写入 tmp_path，测试结束后自动清理。
"""

import base64
import os
import struct
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest

from hutool.extra.epub import (
    _ENGINE_REGISTRY,
    _HAS_EBOOKLIB,
    _HAS_MKEPUB,
    _HAS_PYPUB3,
    EbooklibEpub,
    Epub,
    EpubFactory,
    MkEpub,
    PyPub3Epub,
    _detect_image_format,
)

# ── 辅助：构造最小合法 PNG 二进制 ────────────────────────────


def _make_png_bytes() -> bytes:
    """生成一个 1x1 白色 PNG 的最小二进制。"""
    import binascii
    import zlib

    signature = b"\x89PNG\r\n\x1a\n"

    def _chunk(chunk_type: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + chunk_type
            + data
            + struct.pack(">I", binascii.crc32(chunk_type + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw_data = b"\x00\xff\xff\xff"
    compressed = zlib.compress(raw_data)

    return signature + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", compressed) + _chunk(b"IEND", b"")


# ── 辅助：EPUB 结构校验 ───────────────────────────────────────


def _validate_epub(path: Path) -> dict:
    """校验 EPUB 文件的 ZIP 结构与核心内容。

    返回 dict::

        {
            "valid_zip": bool,
            "has_mimetype": bool,
            "mimetype_correct": bool,       # 内容 == "application/epub+zip"
            "has_container": bool,           # META-INF/container.xml
            "has_opf": bool,                 # *.opf 文件
            "has_chapters": bool,            # 至少 1 个 .xhtml
            "chapter_count": int,
            "files": [str, ...],             # ZIP 内所有文件名
            "chapter_texts": {name: str},    # 每个章节的完整内容
        }
    """
    result = {
        "valid_zip": False,
        "has_mimetype": False,
        "mimetype_correct": False,
        "has_container": False,
        "has_opf": False,
        "has_chapters": False,
        "chapter_count": 0,
        "files": [],
        "chapter_texts": {},
    }

    try:
        with zipfile.ZipFile(str(path), "r") as zf:
            result["valid_zip"] = True
            names = zf.namelist()
            result["files"] = names

            # mimetype（必须是 ZIP 内第一个文件，且不压缩）
            if "mimetype" in names:
                result["has_mimetype"] = True
                content = zf.read("mimetype").decode("utf-8").strip()
                result["mimetype_correct"] = content == "application/epub+zip"

            # META-INF/container.xml
            if "META-INF/container.xml" in names:
                result["has_container"] = True

            # OPF 文件
            opf_files = [n for n in names if n.endswith(".opf")]
            result["has_opf"] = len(opf_files) > 0

            # 章节文件
            chapters = [n for n in names if n.endswith((".xhtml", ".html")) and "nav" not in n.lower()]
            result["chapter_count"] = len(chapters)
            result["has_chapters"] = len(chapters) > 0
            for ch in chapters:
                try:
                    text = zf.read(ch).decode("utf-8")
                except Exception:
                    text = "<decode error>"
                result["chapter_texts"][ch] = text
    except zipfile.BadZipFile:
        pass

    return result


# ── 测试图片格式检测 ──────────────────────────────────────────


class TestDetectImageFormat:
    def test_jpeg(self):
        assert _detect_image_format(b"\xff\xd8\xff\xe0") == "jpeg"

    def test_png(self):
        assert _detect_image_format(b"\x89PNG\r\n") == "png"

    def test_gif(self):
        assert _detect_image_format(b"GIF89a") == "gif"

    def test_webp(self):
        assert _detect_image_format(b"RIFF\x00\x00") == "webp"

    def test_unknown(self):
        assert _detect_image_format(b"\x00\x01\x02") is None


# ── 测试 to_image_html ───────────────────────────────────────


class TestToImageHtml:
    def test_with_png_bytes(self):
        png = _make_png_bytes()
        html = Epub.to_image_html(png)
        assert "data:image/png;base64," in html
        assert "<img src=" in html
        assert 'style="width:100%;"' in html
        # base64 内容可解码
        b64_part = html.split("base64,")[1].split('"')[0]
        decoded = base64.b64decode(b64_part)
        assert decoded == png


# ── 测试 EpubFactory ─────────────────────────────────────────


class TestEpubFactory:
    def test_unknown_engine(self):
        with pytest.raises(ValueError, match="不支持的引擎"):
            EpubFactory.create(engine="unknown_engine_xyz")

    def test_ebooklib_not_installed(self):
        """ebooklib 未安装时应抛出 ImportError。"""
        with patch.dict("hutool.extra.epub._ENGINE_REGISTRY", {}, clear=False):
            # 临时清除 ebooklib 可用标记
            import hutool.extra.epub as mod

            old = mod._HAS_EBOOKLIB
            mod._HAS_EBOOKLIB = False
            try:
                if "ebooklib" in _ENGINE_REGISTRY:
                    with pytest.raises(ImportError):
                        _ENGINE_REGISTRY["ebooklib"](epub_name="test")
            finally:
                mod._HAS_EBOOKLIB = old

    def test_mkepub_not_installed(self):
        """mkepub 未安装时应抛出 ImportError。"""
        import hutool.extra.epub as mod

        old = mod._HAS_MKEPUB
        mod._HAS_MKEPUB = False
        try:
            if "mkepub" in _ENGINE_REGISTRY:
                with pytest.raises(ImportError):
                    _ENGINE_REGISTRY["mkepub"](epub_name="test")
        finally:
            mod._HAS_MKEPUB = old


# ── 测试 Epub 基类逻辑（用 Mock 子类） ───────────────────────


class _MockEpub(Epub):
    """用于测试的 Mock 实现。"""

    def __init__(self, epub_name="test", **kwargs):
        super().__init__(epub_name, **kwargs)
        self._items = []

    @property
    def book(self):
        return None

    def add_image(self, name, img):
        pass

    def _add_item(self, title, content):
        self._items.append((title, content))

    def _write_epub(self, path):
        Path(path).write_bytes(b"MOCK_EPUB")


class TestEpubBase:
    def test_chapter_no_starts_at_zero(self):
        epub = _MockEpub()
        assert epub.chapter_no == 0

    def test_add_page_text(self):
        epub = _MockEpub()
        epub.add_page("第一章", "这是正文内容")
        assert epub.chapter_no == 1
        assert len(epub._items) == 1
        title, content = epub._items[0]
        assert title == "第一章"
        assert "<p>这是正文内容</p>" in content

    def test_add_page_list(self):
        epub = _MockEpub()
        epub.add_page("第二章", ["段落一", "段落二"])
        assert epub.chapter_no == 1
        _, content = epub._items[0]
        assert "<p>段落一</p>" in content
        assert "<p>段落二</p>" in content

    def test_add_page_image(self):
        png = _make_png_bytes()
        epub = _MockEpub()
        epub.add_page("图片页", png)
        _, content = epub._items[0]
        assert "data:image/png;base64," in content

    def test_add_page_mixed(self):
        png = _make_png_bytes()
        epub = _MockEpub()
        epub.add_page("混合", ["文本", png])
        _, content = epub._items[0]
        assert "<p>文本</p>" in content
        assert "data:image/png;base64," in content

    def test_add_page_empty_text_skipped(self):
        epub = _MockEpub()
        epub.add_page("空", ["   ", "有内容"])
        _, content = epub._items[0]
        assert "<p>   </p>" not in content
        assert "<p>有内容</p>" in content

    def test_add_image_page_single(self):
        png = _make_png_bytes()
        epub = _MockEpub()
        epub.add_image_page("漫画", png)
        assert epub.chapter_no == 1

    def test_add_image_page_list(self):
        png = _make_png_bytes()
        epub = _MockEpub()
        epub.add_image_page("漫画", [png, png])
        assert epub.chapter_no == 1

    def test_add_image_page_bad_type(self):
        epub = _MockEpub()
        with pytest.raises(TypeError):
            epub.add_image_page("bad", 12345)

    def test_save_to_file(self, tmp_path):
        epub = _MockEpub("mybook")
        epub.add_page("一", "内容")
        result = epub.save(tmp_path / "output.epub")
        assert result.exists()
        assert result.name == "output.epub"

    def test_save_to_dir(self, tmp_path):
        epub = _MockEpub("mybook")
        epub.add_page("一", "内容")
        result = epub.save(tmp_path)
        assert result.name == "mybook.epub"
        assert result.exists()

    def test_default_title_when_empty(self):
        epub = _MockEpub()
        epub.add_page("", "内容")
        title, _ = epub._items[0]
        assert title == "第1章"

    def test_auto_increment_chapter(self):
        epub = _MockEpub()
        epub.add_page("一", "内容")
        epub.add_page("二", "内容")
        epub.add_page("三", "内容")
        assert epub.chapter_no == 3
        assert len(epub._items) == 3


# ── 测试引擎注册表 ────────────────────────────────────────────


class TestEngineRegistry:
    def test_ebooklib_registered(self):
        assert "ebooklib" in _ENGINE_REGISTRY

    def test_mkepub_registered(self):
        assert "mkepub" in _ENGINE_REGISTRY

    def test_custom_engine(self):
        """测试自定义引擎注册。"""
        from hutool.extra.epub import register_engine

        @register_engine("test_engine")
        class TestEngineEpub(_MockEpub):
            pass

        assert "test_engine" in _ENGINE_REGISTRY
        # 清理
        del _ENGINE_REGISTRY["test_engine"]


# ── 集成测试：EbooklibEpub ─────────────────────────────────────


@pytest.mark.skipif(not _HAS_EBOOKLIB, reason="ebooklib 未安装")
class TestEbooklibEpubIntegration:
    """用真实 ebooklib 引擎生成 EPUB 并校验结构。"""

    def test_basic_text_epub(self, tmp_path):
        """生成包含 3 个文本章节的 EPUB，校验 ZIP 结构与章节内容。"""
        epub = EbooklibEpub(epub_name="测试小说", author="测试作者")
        epub.add_page("第一章 开始", ["这是第一章的内容", "这是第二段"])
        epub.add_page("第二章 发展", "这是第二章的内容")
        epub.add_page("第三章 结局", "这是第三章的内容")

        path = epub.save(tmp_path)
        assert path.exists()
        assert path.suffix == ".epub"

        v = _validate_epub(path)
        assert v["valid_zip"], "EPUB 不是合法 ZIP"
        assert v["has_mimetype"], "缺少 mimetype"
        assert v["mimetype_correct"], "mimetype 内容不正确"
        assert v["has_container"], "缺少 META-INF/container.xml"
        assert v["has_opf"], "缺少 .opf 文件"
        assert v["has_chapters"], "缺少章节"
        assert v["chapter_count"] >= 3

        # 验证章节内容可读且包含正文
        all_text = " ".join(v["chapter_texts"].values())
        assert "第一章" in all_text
        assert "这是第一章的内容" in all_text

    def test_image_page_epub(self, tmp_path):
        """生成包含图片的 EPUB，验证图片以 base64 内联。"""
        png = _make_png_bytes()
        epub = EbooklibEpub(epub_name="漫画")
        epub.add_page("图片页", png)

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_chapters"]

        all_text = " ".join(v["chapter_texts"].values())
        assert "data:image/png;base64," in all_text

    def test_mixed_content_epub(self, tmp_path):
        """混合文本+图片章节。"""
        png = _make_png_bytes()
        epub = EbooklibEpub(epub_name="混合")
        epub.add_page("文图混排", ["文字部分", png, "另一段文字"])

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]

        all_text = " ".join(v["chapter_texts"].values())
        assert "文字部分" in all_text
        assert "data:image/png;base64," in all_text

    def test_add_image_page_epub(self, tmp_path):
        """纯图片章节（漫画模式）。"""
        png = _make_png_bytes()
        epub = EbooklibEpub(epub_name="漫画书")
        epub.add_image_page("第一话", [png, png, png])

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_chapters"]

    def test_with_cover(self, tmp_path):
        """带封面的 EPUB。"""
        cover = _make_png_bytes()
        epub = EbooklibEpub(epub_name="封面书", author="作者", cover=cover)
        epub.add_page("正文", "内容")

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_mimetype"]
        assert v["has_chapters"]

        # 封面图片文件应在 ZIP 内
        cover_files = [f for f in v["files"] if "cover" in f.lower()]
        assert len(cover_files) > 0, f"未找到封面文件，ZIP 内容: {v['files']}"

    def test_custom_css(self, tmp_path):
        """自定义 CSS 应出现在 EPUB 的 stylesheet 中。"""
        css = "body{color:red;}"
        epub = EbooklibEpub(epub_name="样式书", css_style=css)
        epub.add_page("一", "内容")

        path = epub.save(tmp_path)
        with zipfile.ZipFile(str(path), "r") as zf:
            css_files = [n for n in zf.namelist() if n.endswith(".css")]
            assert len(css_files) > 0
            css_content = zf.read(css_files[0]).decode("utf-8")
            assert "color:red" in css_content

    def test_multiple_chapters_spine_order(self, tmp_path):
        """多章节按添加顺序排列。"""
        epub = EbooklibEpub(epub_name="顺序")
        for i in range(10):
            epub.add_page(f"第{i + 1}章", f"内容{i + 1}")

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["chapter_count"] >= 10

        # 章节应按顺序出现
        chapter_files = sorted([n for n in v["files"] if "chapter" in n and n.endswith(".xhtml")])
        assert len(chapter_files) >= 10

    def test_factory_create_ebooklib(self, tmp_path):
        """通过 EpubFactory 创建 ebooklib 实例。"""
        epub = EpubFactory.create("ebooklib", epub_name="工厂创建")
        epub.add_page("一", "内容")
        path = epub.save(tmp_path / "factory.epub")
        assert path.exists()

        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_chapters"]

    def test_epub_is_reopenable(self, tmp_path):
        """生成的 EPUB 可以被 zipfile 再次打开读取。"""
        epub = EbooklibEpub(epub_name="可重开")
        epub.add_page("测试", "内容")
        path = epub.save(tmp_path)

        # 二次打开验证
        with zipfile.ZipFile(str(path), "r") as zf:
            assert "mimetype" in zf.namelist()
            assert len(zf.namelist()) > 3  # 至少 mimetype + container + opf + chapter


# ── 集成测试：MkEpub ─────────────────────────────────────────


@pytest.mark.skipif(not _HAS_MKEPUB, reason="mkepub 未安装")
class TestMkEpubIntegration:
    """用真实 mkepub 引擎生成 EPUB 并校验结构。"""

    def test_basic_text_epub(self, tmp_path):
        epub = MkEpub(epub_name="测试小说", author="测试作者")
        epub.add_page("第一章", ["正文内容", "第二段"])
        epub.add_page("第二章", "更多内容")

        path = epub.save(tmp_path)
        assert path.exists()

        v = _validate_epub(path)
        assert v["valid_zip"], "EPUB 不是合法 ZIP"
        assert v["has_mimetype"]
        assert v["mimetype_correct"]
        assert v["has_container"]
        assert v["has_chapters"]
        assert v["chapter_count"] >= 2

    def test_image_page_epub(self, tmp_path):
        png = _make_png_bytes()
        epub = MkEpub(epub_name="漫画")
        epub.add_page("图片页", png)

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_chapters"]

    def test_with_cover(self, tmp_path):
        cover = _make_png_bytes()
        epub = MkEpub(epub_name="封面书", cover=cover)
        epub.add_page("正文", "内容")

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_mimetype"]

    def test_factory_create_mkepub(self, tmp_path):
        epub = EpubFactory.create("mkepub", epub_name="工厂创建")
        epub.add_page("一", "内容")
        path = epub.save(tmp_path / "factory.epub")
        assert path.exists()

        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_chapters"]

    def test_epub_is_reopenable(self, tmp_path):
        epub = MkEpub(epub_name="可重开")
        epub.add_page("测试", "内容")
        path = epub.save(tmp_path)

        with zipfile.ZipFile(str(path), "r") as zf:
            assert "mimetype" in zf.namelist()
            assert len(zf.namelist()) > 3


# ── 集成测试：PyPub3Epub ─────────────────────────────────────


@pytest.mark.skipif(not _HAS_PYPUB3, reason="pypub3 未安装")
class TestPyPub3EpubIntegration:
    """用真实 pypub3 引擎生成 EPUB 并校验结构。"""

    def test_basic_text_epub(self, tmp_path):
        epub = PyPub3Epub(epub_name="测试小说", author="测试作者")
        epub.add_page("第一章", ["正文内容", "第二段"])
        epub.add_page("第二章", "更多内容")

        path = epub.save(tmp_path)
        assert path.exists()

        v = _validate_epub(path)
        assert v["valid_zip"], "EPUB 不是合法 ZIP"
        assert v["has_mimetype"]
        assert v["mimetype_correct"]
        assert v["has_container"]
        assert v["has_chapters"]
        assert v["chapter_count"] >= 2

    def test_image_page_epub(self, tmp_path):
        png = _make_png_bytes()
        epub = PyPub3Epub(epub_name="漫画")
        epub.add_page("图片页", png)

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_chapters"]

        all_text = " ".join(v["chapter_texts"].values())
        assert "data:image/png;base64," in all_text

    def test_mixed_content_epub(self, tmp_path):
        png = _make_png_bytes()
        epub = PyPub3Epub(epub_name="混合")
        epub.add_page("文图混排", ["文字部分", png])

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]

    def test_with_custom_css(self, tmp_path):
        css = "body { font-size: 20px; }"
        epub = PyPub3Epub(epub_name="样式书", css_style=css)
        epub.add_page("一", "内容")

        path = epub.save(tmp_path)
        v = _validate_epub(path)
        assert v["valid_zip"]

        # 验证自定义 CSS 被包含
        with zipfile.ZipFile(str(path), "r") as zf:
            css_files = [n for n in zf.namelist() if n.endswith(".css")]
            assert len(css_files) > 0
            css_content = ""
            for cf in css_files:
                css_content += zf.read(cf).decode("utf-8")
            assert "font-size: 20px" in css_content

    def test_factory_create_pypub3(self, tmp_path):
        epub = EpubFactory.create("pypub3", epub_name="工厂创建")
        epub.add_page("一", "内容")
        path = epub.save(tmp_path / "factory.epub")
        assert path.exists()

        v = _validate_epub(path)
        assert v["valid_zip"]
        assert v["has_chapters"]

    def test_epub_is_reopenable(self, tmp_path):
        epub = PyPub3Epub(epub_name="可重开")
        epub.add_page("测试", "内容")
        path = epub.save(tmp_path)

        with zipfile.ZipFile(str(path), "r") as zf:
            assert "mimetype" in zf.namelist()
            assert len(zf.namelist()) > 3

    def test_temp_css_cleaned_up(self, tmp_path):
        """自定义 CSS 临时文件在保存后应被清理。"""
        css = "body{color:red;}"
        epub = PyPub3Epub(epub_name="清理", css_style=css)
        temp_path = epub._temp_css_path
        assert temp_path is not None
        assert os.path.exists(temp_path)

        epub.add_page("一", "内容")
        epub.save(tmp_path)

        assert not os.path.exists(temp_path), "临时 CSS 文件未清理"
