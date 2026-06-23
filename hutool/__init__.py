"""Hutool-Python - Java Hutool 的 Python 移植版工具库。

全量移植 Java Hutool 的 Python 版工具库，涵盖：
- core: 核心工具类（字符串、数字、集合、日期、IO、Bean、编解码等）
- http: HTTP 客户端工具
- json: JSON 工具
- crypto: 加密工具（摘要、对称/非对称加密、签名）
- cache: 缓存工具（FIFO、LFU、LRU、定时）
- captcha: 验证码
- dfa: 敏感词过滤
- extra: 扩展工具（拼音、Emoji、模板、二维码）
- cron: 定时任务
- jwt: JWT 工具
- setting: 配置工具（YAML、Properties）
"""

__version__ = "1.1.1"

# 核心工具类 - 顶层快捷导入
# 其他模块
from .cache import CacheUtil, FIFOCache, LFUCache, LRUCache, TimedCache, WeakCache
from .captcha import ArithmeticCaptcha, CaptchaUtil, CircleCaptcha, LineCaptcha
from .core.bank import BankUtil
from .core.bean import BeanUtil
from .core.codec import Base32, Base64
from .core.coll import CollUtil, ListUtil
from .core.date import DateTime, DateUtil
from .core.decorators import (
    CacheFunction,
    FuncOnce,
    Memoize,
    NoneOnException,
    ProfileDeco,
    TimeThis,
    TtlLruCache,
)
from .core.exceptions import ValidateException
from .core.exec import ExecUtil
from .core.io.data_size import DataSizeUtil
from .core.io.file import FileUtil
from .core.io.file_name import FileNameUtil
from .core.io.path import PathUtil
from .core.io.resource import ResourceUtil
from .core.io.streams import IoUtil
from .core.iter import IterUtil
from .core.map import BiMap, DictUtil, MapUtil
from .core.math import BitStatusUtil, MathUtil
from .core.memory_repo import MemoryRepo
from .core.money import MoneyUtil
from .core.net import Ipv4Util, MaskBit, NetUtil
from .core.prof import ProfUtil
from .core.sql import ColumnType, F, Q, SqlUtil
from .core.struct import Struct
from .core.text.csv import CsvUtil
from .core.text.stop_watch import StopWatch, TaskInfo
from .core.text.str_builder import StrBuilder
from .core.text.unicode import UnicodeUtil
from .core.timing import TimingUtil
from .core.tree import TreeNode, TreeUtil
from .core.util.array import ArrayUtil
from .core.util.base32_util import Base32Util
from .core.util.base64_util import Base64Util
from .core.util.boolean import BooleanUtil
from .core.util.charset import CharsetUtil
from .core.util.check import CheckUtil
from .core.util.classes import ClassUtil
from .core.util.color import ColorUtil
from .core.util.convert import ConvertUtil
from .core.util.coordinate import Coordinate, CoordinateUtil
from .core.util.credit_code import CreditCodeUtil
from .core.util.desensitized import DesensitizedUtil
from .core.util.enums import EnumUtil
from .core.util.escape import EscapeUtil
from .core.util.func import FuncUtil
from .core.util.hasher import HashUtil
from .core.util.hex import HexUtil
from .core.util.id import IdUtil
from .core.util.idcard import IdcardUtil
from .core.util.image import ImageUtil
from .core.util.number import NumberUtil
from .core.util.object import ObjectUtil
from .core.util.page import PageUtil
from .core.util.phone import PhoneUtil
from .core.util.randoms import RandomUtil
from .core.util.reflect import ReflectUtil
from .core.util.regex import ReUtil
from .core.util.runtime import RuntimeUtil
from .core.util.strings import CharPool, CharUtil, StrUtil
from .core.util.system import SystemUtil
from .core.util.url import URLUtil
from .core.util.user_agent import UserAgentUtil
from .core.util.version import VersionUtil
from .core.util.xml import XmlUtil
from .core.util.zip import ZipUtil
from .core.workday import WorkdayUtil
from .cron import CronPattern, CronUtil, CronValidator
from .crypto import DigestUtil, SecureUtil, SignUtil
from .dfa import SensitiveUtil
from .extra import (
    AsyncTtsUtil,
    EbooklibEpub,
    EmojiUtil,
    Epub,
    EpubFactory,
    MkEpub,
    PinyinUtil,
    PyPub3Epub,
    QrCodeUtil,
    TemplateUtil,
    TtsUtil,
    TtsVoice,
)
from .httpx_client import HtmlUtil, HttpRequest, HttpResponse, HttpUtil
from .json import JSONUtil
from .jwt import JWTUtil
from .setting import PropsUtil, SettingUtil, YamlUtil

__all__ = [
    "ArithmeticCaptcha",
    "ArrayUtil",
    "AsyncTtsUtil",
    "BankUtil",
    "Base32",
    "Base32Util",
    "Base64",
    "Base64Util",
    "BeanUtil",
    "BiMap",
    "BitStatusUtil",
    "BooleanUtil",
    "CacheFunction",
    "CacheUtil",
    "CaptchaUtil",
    "CharPool",
    "CharUtil",
    "CharsetUtil",
    "CheckUtil",
    "CircleCaptcha",
    "ClassUtil",
    "CollUtil",
    "ColorUtil",
    "ColumnType",
    "ConvertUtil",
    "Coordinate",
    "CoordinateUtil",
    "CreditCodeUtil",
    "CronPattern",
    "CronUtil",
    "CronValidator",
    "CsvUtil",
    "DataSizeUtil",
    "DateTime",
    "DateUtil",
    "DesensitizedUtil",
    "DictUtil",
    "DigestUtil",
    "EbooklibEpub",
    "EmojiUtil",
    "EnumUtil",
    "Epub",
    "EpubFactory",
    "EscapeUtil",
    "ExecUtil",
    "F",
    "FIFOCache",
    "FileNameUtil",
    "FileUtil",
    "FuncOnce",
    "FuncUtil",
    "HashUtil",
    "HexUtil",
    "HtmlUtil",
    "HttpRequest",
    "HttpResponse",
    "HttpUtil",
    "IdUtil",
    "IdcardUtil",
    "ImageUtil",
    "IoUtil",
    "Ipv4Util",
    "IterUtil",
    "JSONUtil",
    "JWTUtil",
    "LFUCache",
    "LRUCache",
    "LineCaptcha",
    "ListUtil",
    "MapUtil",
    "MaskBit",
    "MathUtil",
    "Memoize",
    "MemoryRepo",
    "MkEpub",
    "MoneyUtil",
    "NetUtil",
    "NoneOnException",
    "NumberUtil",
    "ObjectUtil",
    "PageUtil",
    "PathUtil",
    "PhoneUtil",
    "PinyinUtil",
    "ProfUtil",
    "ProfileDeco",
    "PropsUtil",
    "PyPub3Epub",
    "Q",
    "QrCodeUtil",
    "RandomUtil",
    "ReUtil",
    "ReflectUtil",
    "ResourceUtil",
    "RuntimeUtil",
    "SecureUtil",
    "SensitiveUtil",
    "SettingUtil",
    "SignUtil",
    "SqlUtil",
    "StopWatch",
    "StrBuilder",
    "StrUtil",
    "Struct",
    "SystemUtil",
    "TaskInfo",
    "TemplateUtil",
    "TimeThis",
    "TimedCache",
    "TimingUtil",
    "TreeNode",
    "TreeUtil",
    "TtlLruCache",
    "TtsUtil",
    "TtsVoice",
    "URLUtil",
    "UnicodeUtil",
    "UserAgentUtil",
    "ValidateException",
    "VersionUtil",
    "WeakCache",
    "WorkdayUtil",
    "XmlUtil",
    "YamlUtil",
    "ZipUtil",
]
