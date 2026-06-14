<p align="center">
    <h1 align="center">Hutool-Python</h1>
</p>
<p align="center">
    <strong>🐍 A Python utility library ported from Java Hutool</strong>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" />
    <img src="https://img.shields.io/badge/version-1.0.0-green.svg" />
    <img src="https://img.shields.io/badge/license-MulanPSL2-blue.svg" />
    <img src="https://img.shields.io/badge/tests-613 passed-brightgreen.svg" />
    <a href="https://wgp520.github.io/hutool-python/"><img src="https://img.shields.io/badge/docs-online-blueviolet.svg" /></a>
</p>

-------------------------------------------------------------------------------

[**🌎中文说明**](README.md)

-------------------------------------------------------------------------------

## 📚 Introduction

**Hutool-Python** is a Python port of [Java Hutool](https://github.com/dromara/hutool), a comprehensive and easy-to-use Java utility library. Hutool-Python brings Hutool's rich set of tool classes to the Python ecosystem, covering strings, numbers, collections, encoding, dates, files, IO, encryption, JSON, HTTP clients, and more.

### 🍺 Design Philosophy

- **Faithful port**: Class names retain Hutool's PascalCase style (e.g., `StrUtil`, `DateUtil`), while method names follow Python's snake_case convention (e.g., `is_blank`, `offset_day`)
- **Python-native implementation**: Uses Python ecosystem best practices (`pendulum`, `httpx`, `cryptography`, etc.) rather than mechanically translating Java code
- **Chinese documentation**: All docstrings are in Chinese with Sphinx-style formatting (`:param:` / `:return:` / `:raises:`)
- **Zero configuration**: Works out of the box after `pip install`

---

## 🛠️ Modules

| Module | Description | Java Hutool Equivalent |
|--------|-------------|----------------------|
| `core/util/` | Core utilities: string, number, array, object, boolean, random, ID, regex, hash, escape, URL, version, pagination, etc. (25 utility classes) | `cn.hutool.core.util` |
| `core/coll.py` | Collection utilities: `CollUtil`, `ListUtil` | `cn.hutool.core.collection` |
| `core/map.py` | Map utilities: `MapUtil`, `BiMap`, `DictUtil` | `cn.hutool.core.map` |
| `core/io/` | IO utilities: file, IO streams, path, filename, data size, resources (6 classes) | `cn.hutool.core.io` |
| `core/date.py` | Date utilities: `DateUtil`, `DateTime` (powered by pendulum) | `cn.hutool.core.date` |
| `core/bean.py` | Bean utilities: property copy, Map conversion | `cn.hutool.core.bean` |
| `core/codec.py` | Encoding/decoding: `Base64`, `Base32` | `cn.hutool.core.codec` |
| `core/text/` | Text utilities: `UnicodeUtil`, `CsvUtil`, `StrBuilder` | `cn.hutool.core.text` |
| `core/net.py` | Network utilities: `NetUtil`, `Ipv4Util` | `cn.hutool.core.net` |
| `core/math_util.py` | Math utilities: `MathUtil`, `BitStatusUtil` | `cn.hutool.core.math` |
| `core/tree.py` | Tree utilities: `TreeUtil` | `cn.hutool.core.lang.tree` |
| `http/` | HTTP client: `HttpUtil`, `HttpRequest`, `HttpResponse`, `HtmlUtil` (powered by httpx) | `cn.hutool.http` |
| `json_util.py` | JSON utilities: `JSONUtil` (built-in json extension) | `cn.hutool.json` |
| `crypto/` | Encryption: `DigestUtil`, `SecureUtil`, `SignUtil` (powered by cryptography) | `cn.hutool.crypto` |
| `cache/` | Cache: `FIFOCache`, `LFUCache`, `LRUCache`, `TimedCache` | `cn.hutool.cache` |
| `captcha/` | CAPTCHA: `CaptchaUtil` (powered by Pillow) | `cn.hutool.captcha` |
| `dfa/` | Sensitive word filtering: `SensitiveUtil` (DFA algorithm) | `cn.hutool.dfa` |
| `extra/` | Extensions: `EmojiUtil`, `PinyinUtil`, `TemplateUtil`, `QrCodeUtil` | `cn.hutool.extra` |
| `cron/` | Scheduled tasks: `CronUtil`, `CronPattern` | `cn.hutool.cron` |
| `jwt_util.py` | JWT utilities: `JWTUtil` (powered by PyJWT) | `cn.hutool.jwt` |
| `setting/` | Configuration: `SettingUtil`, `YamlUtil`, `PropsUtil` | `cn.hutool.setting` |

> Note: Java-specific modules such as AOP, JDBC, Swing, POI, JNDI, ClassLoader, BloomFilter, Log, Script, Socket, and System are excluded from Hutool-Python.

---

## 📦 Installation

### 🍊 pip (Recommended)

```bash
pip install hutool-python
```

### 🍐 From Source

```bash
git clone https://github.com/wgp520/hutool-python.git
cd hutool-python
pip install -e .
```

### 🧪 With Development Dependencies

```bash
pip install -e ".[dev]"
```

> **Requirements**: Python 3.8+

---

## 🚀 Quick Start

### String Utilities

```python
from hutool import StrUtil

# Check if blank
StrUtil.is_blank("")       # True
StrUtil.is_blank("  ")     # True
StrUtil.is_blank("hello")  # False

# Substring operations
StrUtil.sub_before("abc.jpg", ".")      # "abc"
StrUtil.sub_after("abc.jpg", ".")       # "jpg"
StrUtil.sub_between("a(b)c", "(", ")")  # "b"

# Naming convention conversion
StrUtil.to_camel_case("hello_world")   # "helloWorld"
StrUtil.to_snake_case("helloWorld")    # "hello_world"

# String similarity
StrUtil.similar("I love coding", "I love code")  # 0.857...
```

### Date Utilities

```python
from hutool import DateUtil

# Get current time
DateUtil.now()        # "2024-01-15 14:30:00"
DateUtil.today()      # "2024-01-15"

# Parse dates
dt = DateUtil.parse("2024-01-15")

# Date offset
DateUtil.offset_day(dt, 7)    # 7 days later
DateUtil.offset_month(dt, -1) # 1 month earlier

# Date difference
start = DateUtil.parse("2024-01-01")
end = DateUtil.parse("2024-12-31")
DateUtil.between_day(start, end)  # 365

# Leap year check
DateUtil.is_leap_year(2024)  # True
```

### Collection Utilities

```python
from hutool import CollUtil, MapUtil

# Group by
data = [{"type": "a", "val": 1}, {"type": "b", "val": 2}, {"type": "a", "val": 3}]
CollUtil.group_by(data, key_func=lambda x: x["type"])
# {"a": [{"type": "a", "val": 1}, {"type": "a", "val": 3}], "b": [...]}

# Pagination
CollUtil.page([1, 2, 3, 4, 5], page_num=1, page_size=2)  # [1, 2]

# Map operations
MapUtil.sort({"c": 3, "a": 1, "b": 2})  # {"a": 1, "b": 2, "c": 3}
```

### ID Generation

```python
from hutool import IdUtil

IdUtil.random_uuid()       # "550e8400-e29b-41d4-a716-446655440000"
IdUtil.simple_uuid()       # "550e8400e29b41d4a716446655440000"
IdUtil.nano_id()           # "V1StGXR8_Z5jdHi6B-myT"
IdUtil.snowflake_id()      # 1480946864314982400
IdUtil.object_id()         # "5f8b2c3d4e5f6a7b8c9d0e1f"
```

### HTTP Client

```python
from hutool.http import HttpUtil

# GET request
html = HttpUtil.get("https://example.com")

# POST request
result = HttpUtil.post("https://api.example.com/data", json_data={"key": "value"})

# Chained request builder
from hutool.http import HttpRequest

resp = (HttpRequest.post("https://api.example.com/data")
    .header("Authorization", "Bearer token")
    .json({"key": "value"})
    .timeout(30)
    .execute())

print(resp.is_ok())      # True
print(resp.to_json())    # {...}
```

### Encryption

```python
from hutool.crypto import DigestUtil, SecureUtil

# Digest algorithms
DigestUtil.md5_hex("hello")           # "5d41402abc4b2a76b9719d911017c592"
DigestUtil.sha256_hex("hello")        # "2cf24dba5fb0a30e..."

# AES symmetric encryption
key = SecureUtil.generate_aes_key()
encrypted = SecureUtil.encrypt_aes(b"secret data", key, "ECB")
decrypted = SecureUtil.decrypt_aes(encrypted, key, "ECB")
```

### Sensitive Word Filtering

```python
from hutool.dfa import SensitiveUtil

# Initialize word list
SensitiveUtil.init(["badword", "spam", "forbidden"])

# Detection
SensitiveUtil.contains("This text contains a badword")  # True

# Find all matches
SensitiveUtil.find_all("This text has badword and spam")  # ["badword", "spam"]

# Replace
SensitiveUtil.replace("This text contains a badword")  # "This text contains a *******"
```

### CAPTCHA

```python
from hutool.captcha import CaptchaUtil

# Line-interference CAPTCHA
captcha = CaptchaUtil.create_line_captcha(width=200, height=80, code_count=5)
code = captcha.create_code()
img_bytes = captcha.get_image_bytes()

# Arithmetic CAPTCHA
arith = CaptchaUtil.create_arithmetic_captcha(width=200, height=80)
arith.create_code()        # "3+5=?"
arith.get_result()         # "8"
```

### More Utilities

```python
from hutool.core.util import (
    NumberUtil, ArrayUtil, RandomUtil, HexUtil, HashUtil,
    ReUtil, EscapeUtil, PhoneUtil, IdcardUtil, DesensitizedUtil,
    CoordinateUtil, ZipUtil, XmlUtil, UrlUtil, VersionUtil,
)
from hutool.core.codec import Base64
from hutool.core.io import FileUtil, IoUtil, PathUtil
from hutool.json_util import JSONUtil
from hutool.cache import CacheUtil
from hutool.extra import PinyinUtil, EmojiUtil, TemplateUtil
from hutool.jwt_util import JWTUtil
```

---

## 📁 Project Structure

```
hutool-python/
├── hutool/                    # Python package
│   ├── __init__.py
│   ├── core/                  # Core module (equivalent to hutool-core)
│   │   ├── util/              # Core utilities (25 classes)
│   │   ├── io/                # IO utilities (6 classes)
│   │   ├── text/              # Text utilities (3 classes)
│   │   ├── date.py            # Date utilities
│   │   ├── coll.py            # Collection utilities
│   │   ├── map.py             # Map utilities
│   │   ├── bean.py            # Bean utilities
│   │   ├── codec.py           # Encoding/decoding
│   │   ├── net.py             # Network utilities
│   │   ├── math_util.py       # Math utilities
│   │   └── tree.py            # Tree utilities
│   ├── http/                  # HTTP client (powered by httpx)
│   ├── json_util.py           # JSON utilities
│   ├── crypto/                # Encryption (powered by cryptography)
│   ├── cache/                 # Cache (FIFO/LFU/LRU/Timed)
│   ├── captcha/               # CAPTCHA (powered by Pillow)
│   ├── dfa/                   # Sensitive word filtering (DFA algorithm)
│   ├── extra/                 # Extensions (Pinyin/Emoji/Template/QR Code)
│   ├── cron/                  # Scheduled tasks
│   ├── jwt_util.py            # JWT utilities
│   └── setting/               # Configuration (YAML/Properties)
├── tests/                     # Tests (47 files, 613 test cases)
├── requirements.txt
└── setup.py
```

---

## 🧪 Running Tests

```bash
# Install dev dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run core module tests
pytest tests/test_core/ -v

# Run a single module
pytest tests/test_core/test_str_util.py -v
```

---

## 🔧 Dependencies

| Library | Purpose | Module |
|---------|---------|--------|
| `pendulum>=3.0` | Date/time handling | `core/date.py` |
| `httpx>=0.27` | HTTP client | `http/` |
| `cryptography>=42.0` | Encryption algorithms | `crypto/` |
| `qrcode[pil]>=7.0` | QR code generation | `extra/qr_code_util.py` |
| `Pillow>=10.0` | Image processing (CAPTCHA) | `captcha/` |
| `pypinyin>=0.50` | Chinese Pinyin conversion | `extra/pinyin_util.py` |
| `emoji>=2.0` | Emoji handling | `extra/emoji_util.py` |
| `jinja2>=3.0` | Template engine | `extra/template_util.py` |
| `pyjwt>=2.8` | JWT handling | `jwt_util.py` |
| `pyyaml>=6.0` | YAML parsing | `setting/yaml_util.py` |
| `sortedcontainers>=2.0` | Sorted containers | `cache/` |

---

## 📝 Java Hutool vs Hutool-Python

### Method Name Mapping

| Java Hutool | Hutool-Python | Rule |
|------------|---------------|------|
| `StrUtil.isBlank()` | `StrUtil.is_blank()` | camelCase -> snake_case |
| `DateUtil.offsetDay()` | `DateUtil.offset_day()` | camelCase -> snake_case |
| `new DateTime()` | `DateTime()` | No `new` in Python |
| `CollUtil.newArrayList()` | `CollUtil.new_array_list()` | camelCase -> snake_case |

### Code Comparison

```java
// Java Hutool
String uuid = IdUtil.randomUUID();
boolean blank = StrUtil.isBlank("  ");
DateTime dt = DateUtil.parse("2024-01-15");
String md5 = SecureUtil.md5("hello");
```

```python
# Hutool-Python
uuid = IdUtil.random_uuid()
blank = StrUtil.is_blank("  ")
dt = DateUtil.parse("2024-01-15")
md5 = DigestUtil.md5_hex("hello")
```

---

## 🏗️ Contributing

Contributions are welcome! Please follow these guidelines:

1. **Follow Hutool style**: PascalCase for class names, snake_case for method names
2. **Chinese docstrings**: All new methods must include Chinese documentation in Sphinx style (`:param:` / `:return:` / `:raises:`)
3. **Write tests**: New methods must include pytest test cases
4. **Minimize dependencies**: Prefer Python standard library; add third-party dependencies only when necessary

### Steps

1. Fork the project
2. Create a feature branch (`git checkout -b feature/xxx`)
3. Commit your changes (`git commit -m 'Add xxx feature'`)
4. Push to the branch (`git push origin feature/xxx`)
5. Create a Pull Request

---

## 📖 Related Links

- [Hutool-Python Documentation](https://wgp520.github.io/hutool-python/)
- [Java Hutool Repository](https://github.com/dromara/hutool)
- [Java Hutool Documentation (Chinese)](https://doc.hutool.cn/pages/index/)
- [Hutool API Documentation](https://plus.hutool.cn/apidocs/)

---

## 📄 License

This project is licensed under the [Mulan Permissive Software License, Version 2](https://license.coscl.org.cn/MulanPSL2), consistent with Java Hutool.
