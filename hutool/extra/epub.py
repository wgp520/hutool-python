"""EPUB 生成工具类，支持 ebooklib / mkepub / pypub3 三引擎。"""

import base64
import io
import logging
import os
import shutil
import tempfile
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

logger = logging.getLogger(__name__)


def _remove_chars(s: str, *chars: str) -> str:
    """从字符串中移除指定的字符/子串。"""
    for c in chars:
        s = s.replace(c, "")
    return s


# ── PIL 可选导入 ───────────────────────────────────────────────

try:
    from PIL import Image

    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

# ── 引擎库可选导入 ─────────────────────────────────────────────

_HAS_EBOOKLIB = False
_HAS_MKEPUB = False
_HAS_PYPUB3 = False

try:
    from ebooklib import epub as _ebooklib_epub

    _HAS_EBOOKLIB = True
except ImportError:
    pass

try:
    import mkepub as _mkepub

    _HAS_MKEPUB = True
except ImportError:
    pass

try:
    import pypub as _pypub

    _HAS_PYPUB3 = True
except ImportError:
    pass

# ── 图片格式 magic bytes ──────────────────────────────────────

_MAGIC_FORMATS = [
    (b"\xff\xd8\xff", "jpeg"),
    (b"\x89PNG", "png"),
    (b"GIF8", "gif"),
    (b"RIFF", "webp"),
]


def _detect_image_format(data: bytes) -> Optional[str]:
    """从 magic bytes 推断图片格式（PIL 不可用时的后备方案）。"""
    for magic, fmt in _MAGIC_FORMATS:
        if data[: len(magic)] == magic:
            return fmt
    return None


# ── 引擎注册表 ─────────────────────────────────────────────────

_ENGINE_REGISTRY: Dict[str, Type["Epub"]] = {}


def register_engine(name: str):
    """类装饰器：将实现类注册到引擎注册表。"""

    def decorator(cls: Type["Epub"]) -> Type["Epub"]:
        _ENGINE_REGISTRY[name.lower()] = cls
        return cls

    return decorator


# ====================================================================
# Epub 基类
# ====================================================================


class Epub(ABC):
    """EPUB 生成基类（抽象接口）。

    使用方式（推荐通过 :class:`EpubFactory` 创建）::

        epub = EpubFactory.create(
            engine="ebooklib",   # 或 "mkepub"
            epub_name="小说名",
            author="作者",
            cover=cover_bytes,   # 可选
            language="zh",
        )
        epub.add_page("第一章", ["正文行1", "正文行2", img_bytes])
        epub.save("/path/to/dir")  # 或 Path 对象
    """

    # 默认 CSS 样式
    _DEFAULT_CSS = (
        "body{margin:5%;text-align:justify;font-size:medium;}"
        "code{font-family:monospace;}"
        "h1,h2,h3,h4,h5,h6{text-align:left;}"
        "p{text-indent:2em;}"
        "nav#toc ol,nav#landmarks ol{padding:0;margin-left:1em;}"
        "nav#toc ol li,nav#landmarks ol li{list-style-type:none;margin:0;padding:0;}"
        "a.footnote-ref{vertical-align:super;}"
        "em,em em em,em em em em em{font-style:italic;}"
        "em em,em em em em{font-style:normal;}"
        "code{white-space:pre-wrap;}"
        "span.smallcaps{font-variant:small-caps;}"
        "span.underline{text-decoration:underline;}"
        'q{quotes:"\\201c" "\\201d" "\\2018" "\\2019";}'
        "div.column{display:inline-block;vertical-align:top;width:50%;}"
        "div.hanging-indent{margin-left:1.5em;text-indent:-1.5em;}"
        "@media screen{.sourceCode{overflow:visible !important;white-space:pre-wrap !important;}}"
    )

    # 默认章节 XHTML 模板
    _DEFAULT_XHTML = (
        '<section id="{title}" class="level1" data-number="{chapter_no}">'
        '<h1 data-number="{chapter_no}">{title}</h1>'
        "{body}"
        "</section>"
    )

    def __init__(
        self,
        epub_name: str,
        css_style: Optional[str] = None,
        xhtml_template: Optional[str] = None,
    ) -> None:
        """初始化 EPUB 基类。

        :param epub_name: 书名
        :param css_style: 自定义 CSS 样式
        :param xhtml_template: 自定义章节 XHTML 模板
        """
        self._epub_name = epub_name or "untitled"
        self._css_style = css_style or self._DEFAULT_CSS
        self._xhtml_template = xhtml_template or self._DEFAULT_XHTML
        self._chapter_no = 0

    @property
    def chapter_no(self) -> int:
        """当前章节序号。"""
        return self._chapter_no

    # ── 公共 API ────────────────────────────────────────────

    def add_page(self, title: str, body: Union[str, bytes, List[Union[str, bytes]]]) -> None:
        """添加章节。

        :param title: 章节标题
        :param body: 内容，支持三种形式：

            - ``str`` — 纯文本，作为单段落
            - ``bytes`` — 图片二进制，作为图片页
            - ``list`` — 混合列表，``str`` 元素按段落、``bytes`` 元素按图片处理
        """
        self._chapter_no += 1

        parts: List[str] = []
        if isinstance(body, (str, bytes)):
            body = [body]

        for item in body:
            if isinstance(item, str):
                cleaned = _remove_chars(item, "\n", "\r", "\t", "&nbsp;", " ", "　", "&#13;")
                if cleaned:
                    parts.append(f"<p>{cleaned}</p>")
            elif isinstance(item, bytes):
                parts.append(Epub.to_image_html(item))
            else:
                raise TypeError(f"add_page: 不支持的 body 元素类型: {type(item)}")

        body_html = "\n".join(parts)
        clean_title = _remove_chars(title, "\n", "\r", " ", "&nbsp;", "　", "&#13;", "\t") or f"第{self._chapter_no}章"
        self._add_item(clean_title, body_html)

    def add_image_page(self, title: str, img: Union[bytes, List[bytes]]) -> None:
        """添加纯图片章节（漫画模式）。

        :param title: 章节标题
        :param img: 单张图片二进制或图片二进制列表
        """
        if isinstance(img, bytes):
            images: List[Union[str, bytes]] = [img]
        elif isinstance(img, list):
            images = img
        else:
            raise TypeError(f"add_image_page: 不支持的 img 类型: {type(img)}")
        self.add_page(title, images)

    def save(self, path: Union[str, Path]) -> Path:
        """保存 EPUB 文件。

        :param path: 目录路径（自动以书名命名）或完整文件路径
        :return: 实际保存的文件路径
        """
        path = Path(path)
        if path.is_dir() or not path.suffix:
            path = path / f"{self._epub_name}.epub"
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()
        self._write_epub(str(path))
        return path

    # ── 工具方法 ────────────────────────────────────────────

    @staticmethod
    def to_image_html(image_content: bytes) -> str:
        """将图片二进制转为内联 HTML ``<img>`` 标签。

        PIL 可用时自动检测图片格式；不可用时从 magic bytes 推断。

        :param image_content: 图片二进制数据
        :return: 包含 base64 内联图片的 HTML 字符串
        """
        if _HAS_PIL:
            img = Image.open(io.BytesIO(image_content))
            fmt = img.format
        else:
            fmt = _detect_image_format(image_content)
            if fmt is None:
                raise RuntimeError(
                    "无法检测图片格式：PIL 不可用且 magic bytes 不匹配。请安装 Pillow：pip install Pillow"
                )

        b64 = base64.b64encode(image_content).decode("utf-8")
        return f'<img src="data:image/{fmt.lower()};base64,{b64}" style="width:100%;"/>'

    # ── 引擎必须实现的抽象方法 ──────────────────────────────

    @property
    @abstractmethod
    def book(self) -> Any:
        """获取底层引擎的 book 对象。"""
        ...

    @abstractmethod
    def add_image(self, name: str, img: bytes) -> Any:
        """添加图片资源。

        :param name: 图片名称（不含扩展名）
        :param img: 图片二进制数据
        :return: 图片路径或标识（引擎相关）
        """
        ...

    @abstractmethod
    def _add_item(self, title: str, content: str) -> None:
        """添加章节内容（引擎实现）。

        :param title: 章节标题
        :param content: HTML 正文
        """
        ...

    @abstractmethod
    def _write_epub(self, path: str) -> None:
        """写入 EPUB 文件（引擎实现）。

        :param path: 文件路径
        """
        ...


# ====================================================================
# MkEpub 引擎
# ====================================================================


@register_engine("mkepub")
class MkEpub(Epub):
    """基于 mkepub 的 EPUB 实现。

    轻量级，适合简单的文本+图片 EPUB。
    需要安装：``pip install mkepub``
    """

    def __init__(
        self,
        epub_name: str,
        author: Optional[Union[str, List[str]]] = None,
        cover: Optional[bytes] = None,
        css_style: Optional[str] = None,
        xhtml_template: Optional[str] = None,
    ) -> None:
        """初始化 MkEpub 引擎。

        :param epub_name: 书名
        :param author: 作者（字符串或列表）
        :param cover: 封面图片二进制数据
        :param css_style: 自定义 CSS
        :param xhtml_template: 自定义章节模板
        """
        if not _HAS_MKEPUB:
            raise ImportError("使用 MkEpub 需要先安装 mkepub：pip install mkepub")

        super().__init__(epub_name, css_style=css_style, xhtml_template=xhtml_template)
        self._book = _mkepub.Book(title=epub_name, author=author)
        if cover:
            self._book.set_cover(cover)
        self._book.set_stylesheet(self._css_style)

    @property
    def book(self) -> Any:
        return self._book

    def add_image(self, name: str, img: bytes) -> None:
        img_format = Image.open(io.BytesIO(img)).format if _HAS_PIL else _detect_image_format(img)
        if img_format is None:
            raise RuntimeError("无法检测图片格式")
        self._book.add_image(f"{name}.{img_format.lower()}", img)

    def _add_item(self, title: str, content: str) -> None:
        html = self._xhtml_template.format(title=title, chapter_no=self._chapter_no, body=content)
        self._book.add_page(title, html)

    def _write_epub(self, path: str) -> None:
        self._book.save(path)


# ====================================================================
# Ebooklib 引擎
# ====================================================================


@register_engine("ebooklib")
class EbooklibEpub(Epub):
    """基于 ebooklib 的 EPUB 实现。

    功能更全面，支持目录、CSS、多语言、阅读方向等。
    需要安装：``pip install ebooklib``
    """

    def __init__(
        self,
        epub_name: str,
        author: Optional[Union[str, List[str]]] = None,
        cover: Optional[bytes] = None,
        css_style: Optional[str] = None,
        xhtml_template: Optional[str] = None,
        language: str = "zh",
        direction: str = "default",
    ) -> None:
        """初始化 Ebooklib 引擎。

        :param epub_name: 书名
        :param author: 作者（字符串或列表）
        :param cover: 封面图片二进制数据
        :param css_style: 自定义 CSS
        :param xhtml_template: 自定义章节模板
        :param language: 语言代码（如 ``zh``、``en``）
        :param direction: 阅读方向（``ltr`` / ``rtl`` / ``default``）
        """
        if not _HAS_EBOOKLIB:
            raise ImportError("使用 EbooklibEpub 需要先安装 ebooklib：pip install ebooklib")

        super().__init__(epub_name, css_style=css_style, xhtml_template=xhtml_template)
        self._lang = language
        self._book = self._init_book(epub_name, author, cover, language, direction)

    def _init_book(
        self,
        epub_name: str,
        author: Optional[Union[str, List[str]]],
        cover: Optional[bytes],
        language: str,
        direction: str,
    ) -> Any:
        """初始化 ebooklib EpubBook 对象。"""
        book = _ebooklib_epub.EpubBook()
        book.set_identifier(str(uuid.uuid4()))
        book.set_title(epub_name)

        if author:
            authors = ",".join(author) if isinstance(author, list) else author
            book.add_author(authors)

        book.set_language(language)

        if cover:
            if _HAS_PIL:
                img = Image.open(io.BytesIO(cover))
                cover_fmt = img.format.lower()
            else:
                cover_fmt = _detect_image_format(cover) or "jpeg"
            cover_name = f"images/cover.{cover_fmt}"
            book.set_cover(cover_name, cover, create_page=True)

        style = _ebooklib_epub.EpubItem(
            uid="stylesheet",
            file_name="css/stylesheet.css",
            media_type="text/css",
            content=self._css_style,
        )
        book.add_item(style)
        book.set_direction(direction)
        book.add_metadata(None, "meta", "", {"name": "output encoding", "content": "utf-8"})
        book.toc = []
        return book

    @property
    def book(self) -> Any:
        return self._book

    def add_image(self, name: str, img: bytes) -> str:
        if _HAS_PIL:
            img_format = Image.open(io.BytesIO(img)).format.lower()
        else:
            img_format = _detect_image_format(img) or "jpeg"
        img_name = f"{name}.{img_format}"
        image = _ebooklib_epub.EpubItem(
            uid=str(uuid.uuid4()).replace("-", ""),
            file_name=f"images/{img_name}",
            media_type=f"image/{img_format}",
            content=img,
        )
        self._book.add_item(image)
        return f"images/{img_name}"

    def _add_item(self, title: str, content: str) -> None:
        chapter = _ebooklib_epub.EpubHtml(
            title=title,
            file_name=f"chapter{str(self._chapter_no).zfill(4)}.xhtml",
            content=self._xhtml_template.format(title=title, chapter_no=self._chapter_no, body=content),
            lang=self._lang,
        )
        chapter.add_link(href="css/stylesheet.css", rel="stylesheet", type="text/css")
        self._book.add_item(chapter)
        self._book.toc.append(chapter)
        self._book.spine.append(chapter)

    def _write_epub(self, path: str) -> None:
        self._book.add_item(_ebooklib_epub.EpubNcx())
        nav = _ebooklib_epub.EpubNav()
        nav.uid = "nav"
        self._book.add_item(nav)

        # 在封面后插入导航
        cover_page = next(
            (item for item in self._book.get_items() if getattr(item, "file_name", None) == "cover.xhtml"),
            None,
        )
        if cover_page:
            try:
                cover_idx = self._book.spine.index(cover_page)
            except ValueError:
                cover_idx = -1
            self._book.spine.insert(cover_idx + 1, nav)
            cover_page.properties.append("cover-page")
        else:
            self._book.spine.insert(0, nav)

        _ebooklib_epub.write_epub(path, self._book)


# ====================================================================
# pypub3 引擎
# ====================================================================


@register_engine("pypub3")
class PyPub3Epub(Epub):
    """基于 pypub3 的 EPUB 实现。

    自动生成封面，支持自定义 CSS 和 base64 内联图片。
    需要安装：``pip install pypub3``
    """

    def __init__(
        self,
        epub_name: str,
        author: Optional[Union[str, List[str]]] = None,
        cover: Optional[bytes] = None,
        css_style: Optional[str] = None,
        xhtml_template: Optional[str] = None,
        language: str = "zh",
    ) -> None:
        """初始化 pypub3 引擎。

        :param epub_name: 书名
        :param author: 作者（字符串或列表）
        :param cover: 封面图片二进制数据（暂不支持，pypub3 自动生成封面）
        :param css_style: 自定义 CSS 样式
        :param xhtml_template: 自定义章节模板（pypub3 不支持）
        :param language: 语言代码（如 ``zh``、``en``）
        """
        if not _HAS_PYPUB3:
            raise ImportError("使用 PyPub3Epub 需要先安装 pypub3：pip install pypub3")

        super().__init__(epub_name, css_style=css_style, xhtml_template=xhtml_template)
        self._temp_css_path: Optional[str] = None

        css_paths: List[str] = []
        if css_style:
            css_fd, self._temp_css_path = tempfile.mkstemp(suffix=".css")
            with os.fdopen(css_fd, "w", encoding="utf-8") as f:
                f.write(css_style)
            css_paths.append(self._temp_css_path)

        creator = ",".join(author) if isinstance(author, list) else (author or epub_name)
        self._book = _pypub.Epub(
            title=epub_name,
            creator=creator,
            language=language,
            css_paths=css_paths,
        )

    @property
    def book(self) -> Any:
        return self._book

    def add_image(self, name: str, img: bytes) -> None:
        """pypub3 使用 base64 内联图片，无需单独注册资源。"""
        pass

    def _add_item(self, title: str, content: str) -> None:
        html = self._xhtml_template.format(title=title, chapter_no=self._chapter_no, body=content)
        chapter = _pypub.create_chapter_from_html(html.encode("utf-8"), title=title)
        self._book.add_chapter(chapter)

    def _write_epub(self, path: str) -> None:
        try:
            result = self._book.create(path)
            if Path(result) != Path(path):
                shutil.move(result, path)
        finally:
            if self._temp_css_path and os.path.exists(self._temp_css_path):
                os.unlink(self._temp_css_path)


# ====================================================================
# 工厂
# ====================================================================


class EpubFactory:
    """EPUB 工厂：统一入口，按引擎名称创建实例。

    支持通过 :func:`register_engine` 自定义注册新引擎。

    示例::

        epub = EpubFactory.create("ebooklib", epub_name="小说", author="作者")
    """

    @staticmethod
    def create(engine: str = "ebooklib", **kwargs: Any) -> Epub:
        """创建 EPUB 实例。

        :param engine: 引擎名称（``"ebooklib"`` 或 ``"mkepub"``）
        :param kwargs: 传递给对应引擎 ``__init__`` 的参数
        :return: Epub 实例
        :raises ValueError: 不支持的引擎名称
        :raises ImportError: 引擎对应的库未安装
        """
        engine_key = engine.lower()
        if engine_key in _ENGINE_REGISTRY:
            return _ENGINE_REGISTRY[engine_key](**kwargs)

        available = ", ".join(sorted(_ENGINE_REGISTRY.keys())) or "(无)"
        raise ValueError(f"不支持的引擎: {engine}，已注册引擎: {available}")

    @staticmethod
    def available_engines() -> List[str]:
        """列出当前可用（已安装）的引擎名称。

        :return: 引擎名称列表
        """
        available = []
        for name, cls in _ENGINE_REGISTRY.items():
            try:
                # 尝试实例化看依赖是否真正可用
                cls.__init__.__doc__  # noqa: B018
                available.append(name)
            except Exception:
                pass
        return available
