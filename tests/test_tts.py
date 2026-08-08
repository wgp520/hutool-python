"""TtsUtil / AsyncTtsUtil 模块测试（不依赖网络，mock edge_tts 调用）。"""

import pytest

from hutool.extra.tts import AsyncTtsUtil, TtsUtil, TtsVoice, _filter_voices, _resolve_voice

# ── 测试 TtsVoice 枚举 ──────────────────────────────────────


class TestTtsVoice:
    def test_enum_members(self):
        """枚举应包含预期的中文语音。"""
        assert TtsVoice.XIAO_XIAO.short_name == "zh-CN-XiaoxiaoNeural"
        assert TtsVoice.XIAO_XIAO.gender == "Female"
        assert TtsVoice.XIAO_XIAO.locale == "zh-CN"

    def test_enum_male_voice(self):
        assert TtsVoice.YUN_YANG.short_name == "zh-CN-YunyangNeural"
        assert TtsVoice.YUN_YANG.gender == "Male"

    def test_enum_english_voice(self):
        assert TtsVoice.EN_EMMA.short_name == "en-US-EmmaMultilingualNeural"
        assert TtsVoice.EN_EMMA.locale == "en-US"

    def test_enum_japanese_voice(self):
        assert TtsVoice.JA_NANAMI.short_name == "ja-JP-NanamiNeural"
        assert TtsVoice.JA_NANAMI.locale == "ja-JP"

    def test_enum_korean_voice(self):
        assert TtsVoice.KO_SUNHI.short_name == "ko-KR-SunHiNeural"

    def test_enum_has_all_language_groups(self):
        """应涵盖中/英/日/韩。"""
        locales = {v.locale for v in TtsVoice}
        assert any(l.startswith("zh-CN") for l in locales)
        assert any(l.startswith("en-US") for l in locales)
        assert any(l.startswith("ja-JP") for l in locales)
        assert any(l.startswith("ko-KR") for l in locales)

    def test_iterable(self):
        """枚举可遍历。"""
        voices = list(TtsVoice)
        assert len(voices) > 10


# ── 测试 _resolve_voice ─────────────────────────────────────


class TestResolveVoice:
    def test_with_enum(self):
        assert _resolve_voice(TtsVoice.YUN_YANG) == "zh-CN-YunyangNeural"

    def test_with_string(self):
        assert _resolve_voice("zh-CN-XiaoxiaoNeural") == "zh-CN-XiaoxiaoNeural"

    def test_with_bad_type(self):
        with pytest.raises(TypeError, match="voice 参数类型不正确"):
            _resolve_voice(12345)


# ── 测试 _filter_voices ─────────────────────────────────────


class TestFilterVoices:
    SAMPLE_VOICES = [
        {"ShortName": "zh-CN-XiaoxiaoNeural", "Gender": "Female", "Locale": "zh-CN"},
        {"ShortName": "zh-CN-YunyangNeural", "Gender": "Male", "Locale": "zh-CN"},
        {"ShortName": "en-US-EmmaNeural", "Gender": "Female", "Locale": "en-US"},
        {"ShortName": "ja-JP-NanamiNeural", "Gender": "Female", "Locale": "ja-JP"},
    ]

    def test_filter_by_locale(self):
        result = _filter_voices(self.SAMPLE_VOICES, locale="zh-CN")
        assert len(result) == 2
        assert all(v["Locale"] == "zh-CN" for v in result)

    def test_filter_by_gender(self):
        result = _filter_voices(self.SAMPLE_VOICES, gender="Female")
        assert len(result) == 3

    def test_filter_by_language(self):
        result = _filter_voices(self.SAMPLE_VOICES, language="ja")
        assert len(result) == 1
        assert result[0]["ShortName"] == "ja-JP-NanamiNeural"

    def test_filter_combined(self):
        result = _filter_voices(self.SAMPLE_VOICES, locale="zh-CN", gender="Male")
        assert len(result) == 1
        assert result[0]["ShortName"] == "zh-CN-YunyangNeural"

    def test_filter_no_match(self):
        result = _filter_voices(self.SAMPLE_VOICES, locale="de-DE")
        assert len(result) == 0

    def test_filter_no_criteria(self):
        result = _filter_voices(self.SAMPLE_VOICES)
        assert len(result) == 4


# ── 测试 ImportError 检查（TtsUtil 同步版） ──────────────────


class TestTtsUtilNotInstalled:
    def test_gen_voice_raises(self):
        """未安装 edge_tts 时应抛出 ImportError。"""
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:
            with pytest.raises(ImportError, match="edge_tts"):
                TtsUtil.gen_voice("test")
        finally:
            mod._HAS_EDGE_TTS = old

    def test_gen_voice_bytes_raises(self):
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:
            with pytest.raises(ImportError):
                TtsUtil.gen_voice_bytes("test")
        finally:
            mod._HAS_EDGE_TTS = old

    def test_gen_subtitle_raises(self):
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:
            with pytest.raises(ImportError):
                TtsUtil.gen_subtitle("test")
        finally:
            mod._HAS_EDGE_TTS = old

    def test_stream_voice_raises(self):
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:
            with pytest.raises(ImportError):
                list(TtsUtil.stream_voice("test"))
        finally:
            mod._HAS_EDGE_TTS = old


# ── 测试 ImportError 检查（AsyncTtsUtil 异步版） ─────────────


class TestAsyncTtsUtilNotInstalled:
    @pytest.mark.asyncio
    async def test_gen_voice_raises(self):
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:
            with pytest.raises(ImportError, match="edge_tts"):
                await AsyncTtsUtil.gen_voice("test")
        finally:
            mod._HAS_EDGE_TTS = old

    @pytest.mark.asyncio
    async def test_gen_voice_bytes_raises(self):
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:
            with pytest.raises(ImportError):
                await AsyncTtsUtil.gen_voice_bytes("test")
        finally:
            mod._HAS_EDGE_TTS = old

    @pytest.mark.asyncio
    async def test_gen_subtitle_raises(self):
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:
            with pytest.raises(ImportError):
                await AsyncTtsUtil.gen_subtitle("test")
        finally:
            mod._HAS_EDGE_TTS = old

    @pytest.mark.asyncio
    async def test_stream_voice_raises(self):
        import hutool.extra.tts as mod

        old = mod._HAS_EDGE_TTS
        mod._HAS_EDGE_TTS = False
        try:

            async def _collect():
                async for _ in AsyncTtsUtil.stream_voice("test"):
                    pass

            with pytest.raises(ImportError):
                await _collect()
        finally:
            mod._HAS_EDGE_TTS = old


# ── 用假 edge_tts 模块覆盖异步正向路径（离线） ──────────────


class _FakeCommunicate:
    def __init__(self, *args, **kwargs):
        self._text = kwargs.get("text", "")

    async def stream(self):
        yield {"type": "audio", "data": b"MP3DATA"}
        yield {"type": "WordBoundary", "offset": 0, "duration": 100}

    async def save(self, *args, **kwargs):
        path = args[0] if args else (kwargs.get("output") or "output.mp3")
        with open(path, "wb") as f:
            f.write(b"MP3DATA")


class _FakeSubMaker:
    def feed(self, *a, **k):
        pass

    def get_srt(self):
        return "1\n00:00:00,000 --> 00:00:01,000\nhello\n"


class _FakeEdgeTts:
    Communicate = _FakeCommunicate
    SubMaker = _FakeSubMaker

    @staticmethod
    async def list_voices():
        return []


@pytest.fixture
def mock_edge_tts(monkeypatch):
    import hutool.extra.tts as mod

    monkeypatch.setattr(mod, "_HAS_EDGE_TTS", True, raising=False)
    monkeypatch.setattr(mod, "_edge_tts", _FakeEdgeTts, raising=False)
    yield


class TestAsyncTtsUtilMocked:
    @pytest.mark.asyncio
    async def test_gen_voice_bytes(self, mock_edge_tts):
        data = await AsyncTtsUtil.gen_voice_bytes("你好")
        assert data == b"MP3DATA"

    @pytest.mark.asyncio
    async def test_gen_voice_file(self, mock_edge_tts, tmp_path):
        out = tmp_path / "v.mp3"
        result = await AsyncTtsUtil.gen_voice("你好", output=str(out))
        assert result == out
        assert out.read_bytes() == b"MP3DATA"

    @pytest.mark.asyncio
    async def test_stream_voice(self, mock_edge_tts):
        chunks = []
        async for c in AsyncTtsUtil.stream_voice("你好"):
            chunks.append(c)
        assert chunks == [b"MP3DATA"]

    @pytest.mark.asyncio
    async def test_gen_subtitle(self, mock_edge_tts):
        srt = await AsyncTtsUtil.gen_subtitle("你好")
        assert "hello" in srt
