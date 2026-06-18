<p align="center">
    <h1 align="center">Hutool-Python</h1>
</p>
<p align="center">
    <strong>🐍 让 Python 和 Java 一样"甜蜜"的工具库</strong>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" />
    <a href="https://pypi.org/project/hutool-python/"><img src="https://img.shields.io/pypi/v/hutool-python.svg" /></a>
    <img src="https://img.shields.io/badge/license-MulanPSL2-blue.svg" />
    <img src="https://img.shields.io/badge/tests-2633 passed-brightgreen.svg" />
    <a href="https://wgp520.github.io/hutool-python/"><img src="https://img.shields.io/badge/docs-online-blueviolet.svg" /></a>
</p>

---

[**🌎English Version**](README-EN.md)

---

## 📚 简介

`Hutool-Python` 是 [Java Hutool](https://github.com/dromara/hutool) 的 Python 移植版本，旨在将 Hutool 丰富且易用的工具类生态带到 Python 世界。

**Hutool** 是一个功能丰富且易用的 Java 工具库，涵盖了字符串、数字、集合、编码、日期、文件、IO、加密、JSON、HTTP 客户端等一系列操作。`Hutool-Python` 将这些能力忠实移植到 Python，保留 Hutool 的命名风格和设计理念，让 Java 开发者无缝切换，也让 Python 开发者享受 Hutool 式的便捷体验。

### 🍺 设计理念

- **忠实移植**：类名保持 Hutool 的 PascalCase 风格（如 `StrUtil`、`DateUtil`），方法名转为 Python 的 snake_case（如 `is_blank`、`offset_day`）
- **Python 化实现**：底层实现使用 Python 生态最佳实践（`pendulum`、`httpx`、`cryptography` 等），而非机械翻译 Java 代码
- **中文注释**：所有文档注释均使用中文，采用 Sphinx 风格（`:param:` / `:return:` / `:raises:`），便于源码阅读
- **零配置开箱即用**：无需额外配置，`pip install` 后即可使用

---

## 🛠️ 包含模块

| 模块 | 介绍 | 对应 Java Hutool |
| ---- | ---- | ----------------- |
| `core/util/` | 核心工具类：字符串、数字、数组、对象、布尔、随机、ID、正则、哈希、转义、URL、版本、分页等 | `cn.hutool.core.util` |
| `core/coll.py` | 集合工具：`CollUtil`、`ListUtil` | `cn.hutool.core.collection` |
| `core/map.py` | Map 工具：`MapUtil`、`BiMap`、`DictUtil` | `cn.hutool.core.map` |
| `core/io/` | IO 工具：文件、IO 流、路径、文件名、数据大小、资源 | `cn.hutool.core.io` |
| `core/date.py` | 日期工具：`DateUtil`、`DateTime`（基于 pendulum） | `cn.hutool.core.date` |
| `core/bean.py` | Bean 工具：属性拷贝、Map 互转 | `cn.hutool.core.bean` |
| `core/codec.py` | 编解码：`Base64`、`Base32` | `cn.hutool.core.codec` |
| `core/text/` | 文本工具：`UnicodeUtil`、`CsvUtil`、`StrBuilder` | `cn.hutool.core.text` |
| `core/net.py` | 网络工具：`NetUtil`、`Ipv4Util` | `cn.hutool.core.net` |
| `core/math.py` | 数学工具：`MathUtil`、`BitStatusUtil` | `cn.hutool.core.math` |
| `core/tree.py` | 树工具：`TreeUtil` | `cn.hutool.core.lang.tree` |
| `core/iter.py` | 迭代工具：`IterUtil` | `cn.hutool.core.collection.IterUtil` |
| `httpx_client/` | HTTP 客户端：`HttpUtil`、`HttpRequest`、`HttpResponse`、`HtmlUtil`（基于 httpx） | `cn.hutool.http` |
| `json.py` | JSON 工具：`JSONUtil`（基于内置 json 扩展） | `cn.hutool.json` |
| `crypto/` | 加密工具：`DigestUtil`、`SecureUtil`、`SignUtil`（基于 cryptography） | `cn.hutool.crypto` |
| `cache/` | 缓存工具：`FIFOCache`、`LFUCache`、`LRUCache`、`TimedCache` | `cn.hutool.cache` |
| `captcha/` | 验证码：`CaptchaUtil`（基于 Pillow） | `cn.hutool.captcha` |
| `dfa/` | 敏感词过滤：`SensitiveUtil`（基于 DFA 算法） | `cn.hutool.dfa` |
| `extra/` | 扩展工具：`EmojiUtil`、`PinyinUtil`、`TemplateUtil`、`QrCodeUtil` | `cn.hutool.extra` |
| `cron/` | 定时任务：`CronUtil`、`CronPattern` | `cn.hutool.cron` |
| `jwt.py` | JWT 工具：`JWTUtil`（基于 PyJWT） | `cn.hutool.jwt` |
| `setting/` | 配置工具：`SettingUtil`、`YamlUtil`、`PropsUtil` | `cn.hutool.setting` |

### Python 独有模块

| 模块 | 介绍 |
| ---- | ---- |
| `core/bank.py` | 银行工具：`BankUtil`（IBAN 校验） |
| `core/money.py` | 货币工具：`MoneyUtil`（元/分转换、精确计算） |
| `core/workday.py` | 工作日工具：`WorkdayUtil`（法定节假日） |
| `core/timing.py` | 计时工具：`TimingUtil`（计时器） |
| `core/exec.py` | 并发执行工具：`ExecUtil`（线程池/进程池） |
| `core/prof.py` | 性能分析工具：`ProfUtil`（cProfile） |
| `core/memory_repo.py` | 内存数据仓库：`MemoryRepo`（链式查询） |

> 注：Java Hutool 中的 AOP、JDBC/Swing、POI、JNDI、ClassLoader、BloomFilter、Log、Script、Socket 等 Java 专属模块不包含在 Hutool-Python 中。

---

## 📦 安装

### 🍊 pip 安装（推荐）

```bash
pip install hutool-python
```

### 🍐 从源码安装

```bash
git clone https://github.com/wgp520/hutool-python.git
cd hutool-python
pip install -e .
```

### 🧪 安装开发依赖

```bash
pip install -e ".[dev]"
```

> **要求**：Python 3.8+

---

## 🚀 快速开始

### 字符串工具

```python
from hutool import StrUtil

# 判断是否为空白
StrUtil.is_blank("")       # True
StrUtil.is_blank("  ")     # True
StrUtil.is_blank("hello")  # False

# 子串操作
StrUtil.sub_before("abc.jpg", ".")      # "abc"
StrUtil.sub_after("abc.jpg", ".")       # "jpg"
StrUtil.sub_between("a(b)c", "(", ")")  # "b"

# 命名转换
StrUtil.to_camel_case("hello_world")   # "helloWorld"
StrUtil.to_snake_case("helloWorld")    # "hello_world"

# 字符串相似度
StrUtil.similar("我爱学习", "我爱学")  # 0.75
```

### 日期工具

```python
from hutool import DateUtil

# 获取当前时间
DateUtil.now()        # "2024-01-15 14:30:00"
DateUtil.today()      # "2024-01-15"

# 解析日期
dt = DateUtil.parse("2024-01-15")

# 日期偏移
DateUtil.offset_day(dt, 7)    # 7天后
DateUtil.offset_month(dt, -1) # 1个月前

# 日期差
start = DateUtil.parse("2024-01-01")
end = DateUtil.parse("2024-12-31")
DateUtil.between_day(start, end)  # 365

# 判断闰年
DateUtil.is_leap_year(2024)  # True
```

### 集合工具

```python
from hutool import CollUtil, MapUtil

# 分组
data = [{"type": "a", "val": 1}, {"type": "b", "val": 2}, {"type": "a", "val": 3}]
CollUtil.group_by(data, key_func=lambda x: x["type"])
# {"a": [{"type": "a", "val": 1}, {"type": "a", "val": 3}], "b": [...]}

# 分页
CollUtil.page([1, 2, 3, 4, 5], page_num=1, page_size=2)  # [1, 2]

# Map 操作
MapUtil.sort({"c": 3, "a": 1, "b": 2})  # {"a": 1, "b": 2, "c": 3}
```

### ID 生成

```python
from hutool import IdUtil

IdUtil.random_uuid()       # "550e8400-e29b-41d4-a716-446655440000"
IdUtil.simple_uuid()       # "550e8400e29b41d4a716446655440000"
IdUtil.nano_id()           # "V1StGXR8_Z5jdHi6B-myT"
IdUtil.snowflake_id()      # 1480946864314982400
IdUtil.object_id()         # "5f8b2c3d4e5f6a7b8c9d0e1f"
```

### HTTP 客户端

```python
from hutool import HttpUtil

# GET 请求
html = HttpUtil.get("https://example.com")

# POST 请求
result = HttpUtil.post("https://api.example.com/data", json_data={"key": "value"})

# 链式调用
from hutool import HttpRequest, HttpResponse

resp = (HttpRequest.post("https://api.example.com/data")
    .header("Authorization", "Bearer token")
    .json({"key": "value"})
    .timeout(30)
    .execute())

print(resp.is_ok())      # True
print(resp.to_json())    # {...}
```

### 加密工具

```python
from hutool.crypto import DigestUtil, SecureUtil

# 摘要算法
DigestUtil.md5_hex("hello")           # "5d41402abc4b2a76b9719d911017c592"
DigestUtil.sha256_hex("hello")        # "2cf24dba5fb0a30e..."

# AES 对称加密
key = SecureUtil.generate_aes_key()
encrypted = SecureUtil.encrypt_aes(b"secret data", key, "ECB")
decrypted = SecureUtil.decrypt_aes(encrypted, key, "ECB")
```

### 敏感词过滤

```python
from hutool.dfa import SensitiveUtil

# 初始化敏感词库
SensitiveUtil.init(["敏感词", "违禁词", "垃圾信息"])

# 检测
SensitiveUtil.contains("这是一段包含敏感词的文本")  # True

# 查找
SensitiveUtil.find_all("这是一段包含敏感词和违禁词的文本")  # ["敏感词", "违禁词"]

# 替换
SensitiveUtil.replace("这是一段包含敏感词的文本")  # "这是一段包含**的文本"
```

### 验证码

```python
from hutool.captcha import CaptchaUtil

# 线干扰验证码
captcha = CaptchaUtil.create_line_captcha(width=200, height=80, code_count=5)
code = captcha.create_code()
img_bytes = captcha.get_image_bytes()

# 算术验证码
arith = CaptchaUtil.create_arithmetic_captcha(width=200, height=80)
arith.create_code()        # "3+5=?"
arith.get_result()         # "8"
```

### 更多工具

```python
from hutool.core.util import (
    NumberUtil, ArrayUtil, RandomUtil, HexUtil, HashUtil,
    ReUtil, EscapeUtil, PhoneUtil, IdcardUtil, DesensitizedUtil,
    CoordinateUtil, ZipUtil, XmlUtil, UrlUtil, VersionUtil,
)
from hutool.core.codec import Base64
from hutool.core.io import FileUtil, IoUtil, PathUtil
from hutool import JSONUtil
from hutool.cache import CacheUtil
from hutool.extra import PinyinUtil, EmojiUtil, TemplateUtil
from hutool import JWTUtil
```

---

## 📁 项目结构

```text
hutool-python/
├── hutool/                    # Python 包
│   ├── __init__.py
│   ├── core/                  # 核心模块（对应 hutool-core）
│   │   ├── util/              # 核心工具类（32 个）
│   │   ├── io/                # IO 工具类（6 个）
│   │   ├── text/              # 文本工具类（3 个）
│   │   ├── date.py            # 日期工具
│   │   ├── coll.py            # 集合工具
│   │   ├── map.py             # Map 工具
│   │   ├── bean.py            # Bean 工具
│   │   ├── codec.py           # 编解码工具
│   │   ├── net.py             # 网络工具
│   │   ├── math.py            # 数学工具
│   │   ├── tree.py            # 树工具
│   │   ├── bank.py            # 银行工具（IBAN）
│   │   ├── money.py           # 货币工具
│   │   ├── workday.py         # 工作日工具
│   │   ├── iter.py            # 迭代工具
│   │   ├── timing.py          # 计时工具
│   │   ├── exec.py            # 并发执行工具
│   │   ├── prof.py            # 性能分析工具
│   │   └── memory_repo.py     # 内存数据仓库
│   ├── httpx_client/          # HTTP 客户端（基于 httpx）
│   ├── json.py                # JSON 工具
│   ├── crypto/                # 加密工具（基于 cryptography）
│   ├── cache/                 # 缓存工具（FIFO/LFU/LRU/Timed）
│   ├── captcha/               # 验证码（基于 Pillow）
│   ├── dfa/                   # 敏感词过滤（DFA 算法）
│   ├── extra/                 # 扩展工具（拼音/Emoji/模板/二维码）
│   ├── cron/                  # 定时任务
│   ├── jwt.py                 # JWT 工具
│   └── setting/               # 配置工具（YAML/Properties）
├── tests/                     # 测试（61 个测试文件，1199 个测试用例）
├── requirements.txt
└── setup.py
```

---

## 🧪 运行测试

```bash
# 安装开发依赖
pip install pytest ruff

# 运行全部测试
pytest tests/ -v

# 运行核心模块测试
pytest tests/test_core/ -v

# 运行单个模块测试
pytest tests/test_core/test_strings.py -v
```

### 🔍 代码质量检查（Ruff）

本项目使用 [Ruff](https://docs.astral.sh/ruff/) 进行代码风格检查和格式化：

```bash
# 安装 ruff
pip install ruff

# 代码风格检查
ruff check .

# 代码风格检查并自动修复
ruff check --fix .

# 代码格式化
ruff format .

# 一键执行检查 + 格式化（推荐提交前运行）
ruff check --fix . && ruff format .
```

---

## 🔧 依赖清单

| 依赖库 | 用途 | 对应模块 |
| ------ | ---- | ------- |
| `pendulum>=3.0` | 日期时间处理 | `core/date.py` |
| `httpx>=0.27` | HTTP 客户端 | `httpx_client/` |
| `cryptography>=42.0` | 加密算法 | `crypto/` |
| `qrcode[pil]>=7.0` | 二维码生成 | `extra/qr_code.py` |
| `Pillow>=10.0` | 图像处理（验证码） | `captcha/` |
| `pypinyin>=0.50` | 中文拼音转换 | `extra/pinyin.py` |
| `emoji>=2.0` | Emoji 处理 | `extra/emoji.py` |
| `jinja2>=3.0` | 模板引擎 | `extra/template.py` |
| `pyjwt>=2.8` | JWT 处理 | `jwt.py` |
| `pyyaml>=6.0` | YAML 解析 | `setting/yaml.py` |
| `sortedcontainers>=2.0` | 有序容器 | `cache/` |
| `pytz>=2023.3` | 时区处理 | `core/date.py` |
| `bcrypt>=4.0` | bcrypt 加密 | `crypto/` |

---

## 📝 Java Hutool 与 Hutool-Python 对照

### 方法名映射规则

| Java Hutool | Hutool-Python | 示例 |
| ------------ | --------------- | ---- |
| `StrUtil.isBlank()` | `StrUtil.is_blank()` | 驼峰 → 蛇形 |
| `DateUtil.offsetDay()` | `DateUtil.offset_day()` | 驼峰 → 蛇形 |
| `new DateTime()` | `DateTime()` | Python 无 `new` |
| `CollUtil.newArrayList()` | `CollUtil.new_array_list()` | 驼峰 → 蛇形 |

### 使用对比

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

## 🏗️ 贡献指南

欢迎为 Hutool-Python 贡献代码！请遵循以下原则：

1. **保持 Hutool 风格**：类名使用 PascalCase，方法名使用 snake_case
2. **中文注释**：所有新增方法须包含中文文档注释，格式为 Sphinx 风格（`:param:` / `:return:` / `:raises:`）
3. **编写测试**：新增方法须附带 pytest 测试用例
4. **代码检查**：提交前运行 `ruff check hutool/ tests/ --fix && ruff format hutool/ tests/` 确保代码风格一致
5. **不引入额外依赖**：尽量使用 Python 标准库，仅在必要时引入第三方依赖

### 贡献步骤

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/xxx`)
3. 提交代码 (`git commit -m 'Add xxx feature'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

---

## 📖 相关链接

- [PyPI](https://pypi.org/project/hutool-python/)
- [Hutool-Python 在线文档](https://wgp520.github.io/hutool-python/)
- [Java Hutool 官方仓库](https://github.com/dromara/hutool)
- [Java Hutool 中文文档](https://doc.hutool.cn/pages/index/)
- [Hutool API 文档](https://plus.hutool.cn/apidocs/)

---

## 📄 许可证

本项目基于 [木兰宽松许可证, 第2版](https://license.coscl.org.cn/MulanPSL2) 开源，与 Java Hutool 保持一致。
