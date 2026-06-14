"""Hutool-Python - Java Hutool 的 Python 移植版工具库。

全量移植 Java Hutool 的 Python 版工具库，涵盖：
- core: 核心工具类（字符串、数字、集合、日期、IO、Bean、编解码等）
- http: HTTP 客户端工具
- json_util: JSON 工具
- crypto: 加密工具（摘要、对称/非对称加密、签名）
- cache: 缓存工具（FIFO、LFU、LRU、定时）
- captcha: 验证码
- dfa: 敏感词过滤
- extra: 扩展工具（拼音、Emoji、模板、二维码）
- cron: 定时任务
- jwt_util: JWT 工具
- setting: 配置工具（YAML、Properties）
"""

__version__ = "1.0.0"

# 核心工具类 - 顶层快捷导入
from .core.bean import BeanUtil
from .core.codec import Base32, Base64
from .core.coll import CollUtil, ListUtil
from .core.date import DateTime, DateUtil
from .core.io.data_size_util import DataSizeUtil
from .core.io.file_name_util import FileNameUtil
from .core.io.file_util import FileUtil
from .core.io.io_util import IoUtil
from .core.io.path_util import PathUtil
from .core.io.resource_util import ResourceUtil
from .core.map import BiMap, DictUtil, MapUtil
from .core.math_util import BitStatusUtil, MathUtil
from .core.net import Ipv4Util, MaskBit, NetUtil
from .core.text.csv_util import CsvUtil
from .core.text.str_builder import StrBuilder
from .core.text.unicode_util import UnicodeUtil
from .core.tree import TreeNode, TreeUtil
from .core.util.array_util import ArrayUtil
from .core.util.boolean_util import BooleanUtil
from .core.util.charset_util import CharsetUtil
from .core.util.class_util import ClassUtil
from .core.util.coordinate_util import Coordinate, CoordinateUtil
from .core.util.credit_code_util import CreditCodeUtil
from .core.util.desensitized_util import DesensitizedUtil
from .core.util.enum_util import EnumUtil
from .core.util.escape_util import EscapeUtil
from .core.util.hash_util import HashUtil
from .core.util.hex_util import HexUtil
from .core.util.id_util import IdUtil
from .core.util.idcard_util import IdcardUtil
from .core.util.number_util import NumberUtil
from .core.util.object_util import ObjectUtil
from .core.util.page_util import PageUtil
from .core.util.phone_util import PhoneUtil
from .core.util.random_util import RandomUtil
from .core.util.re_util import ReUtil
from .core.util.reflect_util import ReflectUtil
from .core.util.runtime_util import RuntimeUtil
from .core.util.str_util import CharPool, CharUtil, StrUtil
from .core.util.system_util import SystemUtil
from .core.util.url_util import URLUtil
from .core.util.version_util import VersionUtil
from .core.util.xml_util import XmlUtil
from .core.util.zip_util import ZipUtil

# 其他模块
from .cache import CacheUtil, FIFOCache, LFUCache, LRUCache, TimedCache
from .captcha import ArithmeticCaptcha, CaptchaUtil, LineCaptcha
from .crypto import DigestUtil, SecureUtil, SignUtil
from .cron import CronPattern, CronUtil
from .dfa import SensitiveUtil
from .extra import EmojiUtil, PinyinUtil, QrCodeUtil, TemplateUtil
from .http import HtmlUtil, HttpRequest, HttpResponse, HttpUtil
from .json_util import JSONUtil
from .jwt_util import JWTUtil
from .setting import PropsUtil, SettingUtil, YamlUtil

__all__ = [
    # core/util
    "ArrayUtil",
    "BooleanUtil",
    "CharsetUtil",
    "CharPool",
    "CharUtil",
    "ClassUtil",
    "Coordinate",
    "CoordinateUtil",
    "CreditCodeUtil",
    "DesensitizedUtil",
    "EnumUtil",
    "EscapeUtil",
    "HashUtil",
    "HexUtil",
    "IdUtil",
    "IdcardUtil",
    "NumberUtil",
    "ObjectUtil",
    "PageUtil",
    "PhoneUtil",
    "RandomUtil",
    "ReUtil",
    "ReflectUtil",
    "RuntimeUtil",
    "StrUtil",
    "SystemUtil",
    "URLUtil",
    "VersionUtil",
    "XmlUtil",
    "ZipUtil",
    # core/io
    "DataSizeUtil",
    "FileNameUtil",
    "FileUtil",
    "IoUtil",
    "PathUtil",
    "ResourceUtil",
    # core/text
    "CsvUtil",
    "StrBuilder",
    "UnicodeUtil",
    # core 其他
    "Base32",
    "Base64",
    "BeanUtil",
    "BiMap",
    "BitStatusUtil",
    "CollUtil",
    "DateTime",
    "DateUtil",
    "DictUtil",
    "Ipv4Util",
    "ListUtil",
    "MapUtil",
    "MaskBit",
    "MathUtil",
    "NetUtil",
    "TreeNode",
    "TreeUtil",
    # http
    "HtmlUtil",
    "HttpRequest",
    "HttpResponse",
    "HttpUtil",
    # json / jwt
    "JSONUtil",
    "JWTUtil",
    # cache
    "CacheUtil",
    "FIFOCache",
    "LFUCache",
    "LRUCache",
    "TimedCache",
    # captcha
    "ArithmeticCaptcha",
    "CaptchaUtil",
    "LineCaptcha",
    # crypto
    "DigestUtil",
    "SecureUtil",
    "SignUtil",
    # cron
    "CronPattern",
    "CronUtil",
    # dfa
    "SensitiveUtil",
    # extra
    "EmojiUtil",
    "PinyinUtil",
    "QrCodeUtil",
    "TemplateUtil",
    # setting
    "PropsUtil",
    "SettingUtil",
    "YamlUtil",
]
