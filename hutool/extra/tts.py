"""TTS 文字转语音工具类，基于 edge_tts。

提供两个工具类：

- :class:`TtsUtil` — 同步版本
- :class:`AsyncTtsUtil` — 异步版本（方法名与同步版一致）
"""

import asyncio
import logging
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

# ── edge_tts 可选导入 ─────────────────────────────────────────

_HAS_EDGE_TTS = False

try:
    import edge_tts as _edge_tts

    _HAS_EDGE_TTS = True
except Exception:
    pass


# ====================================================================
# 常用语音枚举
# ====================================================================


class TtsVoice(Enum):
    """常用语音列表（基于 Microsoft Edge TTS）。

    每个成员的值为 ``(short_name, gender, locale)`` 三元组。
    """

    # ── 中文（普通话） ────────────────────────────────────
    XIAO_XIAO = ("zh-CN-XiaoxiaoNeural", "Female", "zh-CN")
    XIAO_YI = ("zh-CN-XiaoyiNeural", "Female", "zh-CN")
    YUN_JIAN = ("zh-CN-YunjianNeural", "Male", "zh-CN")
    YUN_XI = ("zh-CN-YunxiNeural", "Male", "zh-CN")
    YUN_XIA = ("zh-CN-YunxiaNeural", "Male", "zh-CN")
    YUN_YANG = ("zh-CN-YunyangNeural", "Male", "zh-CN")
    XIAO_BEI = ("zh-CN-liaoning-XiaobeiNeural", "Female", "zh-CN-liaoning")
    XIAO_NI = ("zh-CN-shaanxi-XiaoniNeural", "Female", "zh-CN-shaanxi")

    # ── 中文（粤语） ──────────────────────────────────────
    HIU_GAAI = ("zh-HK-HiuGaaiNeural", "Female", "zh-HK")
    HIU_MAAN = ("zh-HK-HiuMaanNeural", "Female", "zh-HK")
    WAN_LUNG = ("zh-HK-WanLungNeural", "Male", "zh-HK")

    # ── 中文（台湾） ──────────────────────────────────────
    HSIAO_CHEN = ("zh-TW-HsiaoChenNeural", "Female", "zh-TW")
    YUN_JHE = ("zh-TW-YunJheNeural", "Male", "zh-TW")
    HSIAO_YU = ("zh-TW-HsiaoYuNeural", "Female", "zh-TW")

    # ── 英语 ──────────────────────────────────────────────
    EN_EMMA = ("en-US-EmmaMultilingualNeural", "Female", "en-US")
    EN_ANDREW = ("en-US-AndrewNeural", "Male", "en-US")
    EN_BRIAN = ("en-US-BrianNeural", "Male", "en-US")
    EN_JENNY = ("en-US-JennyNeural", "Female", "en-US")
    EN_GUY = ("en-US-GuyNeural", "Male", "en-US")
    EN_ARIA = ("en-US-AriaNeural", "Female", "en-US")

    # ── 日语 ──────────────────────────────────────────────
    JA_NANAMI = ("ja-JP-NanamiNeural", "Female", "ja-JP")
    JA_KEITA = ("ja-JP-KeitaNeural", "Male", "ja-JP")

    # ── 韩语 ──────────────────────────────────────────────
    KO_SUNHI = ("ko-KR-SunHiNeural", "Female", "ko-KR")
    KO_INJUN = ("ko-KR-InJoonNeural", "Male", "ko-KR")

    def __init__(self, short_name: str, gender: str, locale: str) -> None:
        self.short_name = short_name
        self.gender = gender
        self.locale = locale


# ====================================================================
# TtsUtil — 同步版本
# ====================================================================


class TtsUtil:
    """文字转语音工具（同步版），基于 Microsoft Edge TTS 服务。

    所有方法均为静态方法，阻塞式调用。

    需要安装：``pip install edge_tts``

    异步版本请使用 :class:`AsyncTtsUtil`，方法名完全一致。
    """

    # ── 语音列表 ──────────────────────────────────────────

    @staticmethod
    def list_voices() -> List[Dict[str, Any]]:
        """列出所有可用语音。

        :return: 语音列表，每个元素为包含 ``ShortName``、``Gender``、``Locale`` 等字段的字典
        """
        return asyncio.run(_edge_tts.list_voices())

    @staticmethod
    def find_voices(
        *,
        locale: Optional[str] = None,
        gender: Optional[str] = None,
        language: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """按条件查找语音。

        :param locale: 地区代码（如 ``zh-CN``、``en-US``）
        :param gender: 性别（``Male`` / ``Female``）
        :param language: 语言代码（如 ``zh``、``en``）
        :return: 匹配的语音列表
        """
        return _filter_voices(TtsUtil.list_voices(), locale=locale, gender=gender, language=language)

    # ── 生成到文件 ────────────────────────────────────────

    @staticmethod
    def gen_voice(
        text: str,
        output: Union[str, Path] = "output.mp3",
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
        subtitle_file: Optional[Union[str, Path]] = None,
    ) -> Path:
        """将文字转为语音并保存到文件。

        :param text: 要转换的文字
        :param output: 输出文件路径（默认 ``output.mp3``）
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速（如 ``+20%``、``-10%``）
        :param volume: 音量（如 ``+50%``、``-20%``）
        :param pitch: 音调（如 ``+10Hz``、``-5Hz``）
        :param proxy: 代理地址（如 ``http://127.0.0.1:7890``）
        :param subtitle_file: 字幕文件路径（可选，生成 SRT 格式）
        :return: 输出文件路径
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)
        output = str(output)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        if subtitle_file:
            communicate.save_sync(output, metadata_fname=str(subtitle_file))
        else:
            communicate.save_sync(output)

        return Path(output)

    # ── 生成为 bytes ──────────────────────────────────────

    @staticmethod
    def gen_voice_bytes(
        text: str,
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ) -> bytes:
        """将文字转为语音并返回 MP3 二进制。

        :param text: 要转换的文字
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :return: MP3 音频二进制数据
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        audio = bytearray()
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
        return bytes(audio)

    # ── 字幕生成 ──────────────────────────────────────────

    @staticmethod
    def gen_subtitle(
        text: str,
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ) -> str:
        """生成文字对应的 SRT 字幕。

        :param text: 要转换的文字
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :return: SRT 格式字幕字符串
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        sub = _edge_tts.SubMaker()
        for chunk in communicate.stream_sync():
            if chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                sub.feed(chunk)
        return sub.get_srt()

    # ── 批量生成 ──────────────────────────────────────────

    @staticmethod
    def gen_all_voices(
        text: str,
        output_dir: Union[str, Path] = "data/tts",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ) -> List[Path]:
        """使用所有内置语音生成音频文件。

        :param text: 要转换的文字
        :param output_dir: 输出目录
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :return: 生成的文件路径列表
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results: List[Path] = []
        for voice in TtsVoice:
            filename = output_dir / f"{voice.short_name}.mp3"
            TtsUtil.gen_voice(
                text=text, output=filename, voice=voice, rate=rate, volume=volume, pitch=pitch, proxy=proxy
            )
            results.append(filename)
        return results

    # ── 流式音频 ──────────────────────────────────────────

    @staticmethod
    def stream_voice(
        text: str,
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ):
        """流式获取音频数据（同步生成器）。

        每次 yield 一个 MP3 音频片段（bytes）。

        :param text: 要转换的文字
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :yield: MP3 音频片段
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                yield chunk["data"]


# ====================================================================
# AsyncTtsUtil — 异步版本
# ====================================================================


class AsyncTtsUtil:
    """文字转语音工具（异步版），基于 Microsoft Edge TTS 服务。

    所有方法均为 ``async`` 静态方法，需在协程中调用。

    方法名与 :class:`TtsUtil` 完全一致，仅调用方式不同：

    .. code-block:: python

        import asyncio
        from hutool import AsyncTtsUtil

        asyncio.run(AsyncTtsUtil.gen_voice("你好", output="hello.mp3"))

    需要安装：``pip install edge_tts``
    """

    # ── 语音列表 ──────────────────────────────────────────

    @staticmethod
    async def list_voices() -> List[Dict[str, Any]]:
        """列出所有可用语音。

        :return: 语音列表
        """
        return await _edge_tts.list_voices()

    @staticmethod
    async def find_voices(
        *,
        locale: Optional[str] = None,
        gender: Optional[str] = None,
        language: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """按条件查找语音。

        :param locale: 地区代码
        :param gender: 性别
        :param language: 语言代码
        :return: 匹配的语音列表
        """
        all_voices = await AsyncTtsUtil.list_voices()
        return _filter_voices(all_voices, locale=locale, gender=gender, language=language)

    # ── 生成到文件 ────────────────────────────────────────

    @staticmethod
    async def gen_voice(
        text: str,
        output: Union[str, Path] = "output.mp3",
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
        subtitle_file: Optional[Union[str, Path]] = None,
    ) -> Path:
        """将文字转为语音并保存到文件。

        :param text: 要转换的文字
        :param output: 输出文件路径
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :param subtitle_file: 字幕文件路径（可选）
        :return: 输出文件路径
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)
        output = str(output)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        if subtitle_file:
            await communicate.save(output, metadata_fname=str(subtitle_file))
        else:
            await communicate.save(output)

        return Path(output)

    # ── 生成为 bytes ──────────────────────────────────────

    @staticmethod
    async def gen_voice_bytes(
        text: str,
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ) -> bytes:
        """将文字转为语音并返回 MP3 二进制。

        :param text: 要转换的文字
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :return: MP3 音频二进制数据
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        audio = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
        return bytes(audio)

    # ── 字幕生成 ──────────────────────────────────────────

    @staticmethod
    async def gen_subtitle(
        text: str,
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ) -> str:
        """生成文字对应的 SRT 字幕。

        :param text: 要转换的文字
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :return: SRT 格式字幕字符串
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        sub = _edge_tts.SubMaker()
        async for chunk in communicate.stream():
            if chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                sub.feed(chunk)
        return sub.get_srt()

    # ── 批量生成 ──────────────────────────────────────────

    @staticmethod
    async def gen_all_voices(
        text: str,
        output_dir: Union[str, Path] = "data/tts",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ) -> List[Path]:
        """使用所有内置语音生成音频文件。

        :param text: 要转换的文字
        :param output_dir: 输出目录
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :return: 生成的文件路径列表
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results: List[Path] = []
        for voice in TtsVoice:
            filename = output_dir / f"{voice.short_name}.mp3"
            await AsyncTtsUtil.gen_voice(
                text=text, output=filename, voice=voice, rate=rate, volume=volume, pitch=pitch, proxy=proxy
            )
            results.append(filename)
        return results

    # ── 流式音频 ──────────────────────────────────────────

    @staticmethod
    async def stream_voice(
        text: str,
        voice: Union[str, TtsVoice] = TtsVoice.YUN_YANG,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        proxy: Optional[str] = None,
    ):
        """流式获取音频数据（异步生成器）。

        每次 yield 一个 MP3 音频片段（bytes）。

        :param text: 要转换的文字
        :param voice: 语音名称字符串或 :class:`TtsVoice` 枚举
        :param rate: 语速
        :param volume: 音量
        :param pitch: 音调
        :param proxy: 代理地址
        :yield: MP3 音频片段
        """
        _check_edge_tts()
        voice_name = _resolve_voice(voice)

        communicate = _edge_tts.Communicate(
            text=text, voice=voice_name, rate=rate, volume=volume, pitch=pitch, proxy=proxy
        )

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]


# ====================================================================
# 内部工具函数
# ====================================================================


def _check_edge_tts() -> None:
    """检查 edge_tts 是否可用。"""
    if not _HAS_EDGE_TTS:
        raise ImportError("使用 TtsUtil/AsyncTtsUtil 需要先安装 edge_tts：pip install edge_tts")


def _resolve_voice(voice: Union[str, "TtsVoice"]) -> str:
    """将语音参数解析为 short_name 字符串。"""
    if isinstance(voice, TtsVoice):
        return voice.short_name
    if isinstance(voice, str):
        return voice
    raise TypeError(f"voice 参数类型不正确: {type(voice)}，应为 str 或 TtsVoice")


def _filter_voices(
    voices: List[Dict[str, Any]],
    *,
    locale: Optional[str] = None,
    gender: Optional[str] = None,
    language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """按条件过滤语音列表。"""
    result = voices
    if locale:
        result = [v for v in result if v.get("Locale", "").startswith(locale)]
    if gender:
        result = [v for v in result if v.get("Gender") == gender]
    if language:
        result = [v for v in result if v.get("Locale", "").startswith(language)]
    return result
