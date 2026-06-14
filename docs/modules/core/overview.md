# 核心模块概述

`hutool.core` 是 Hutool-Python 的核心模块，提供了最基础、最常用的工具类。

## 模块列表

### 工具类 (core/util/)

| 工具类 | 说明 |
|--------|------|
| `StrUtil` | 字符串工具 |
| `NumberUtil` | 数字工具 |
| `ArrayUtil` | 数组工具 |
| `ObjectUtil` | 对象工具 |
| `BooleanUtil` | 布尔工具 |
| `RandomUtil` | 随机工具 |
| `IdUtil` | ID 生成工具 |
| `HexUtil` | 十六进制工具 |
| `HashUtil` | 哈希算法 |
| `ReUtil` | 正则工具 |
| `EscapeUtil` | 转义工具 |
| `URLUtil` | URL 工具 |
| `XmlUtil` | XML 工具 |
| `DesensitizedUtil` | 信息脱敏 |
| `IdcardUtil` | 身份证工具 |
| `PhoneUtil` | 手机号工具 |
| `CoordinateUtil` | 坐标转换 |
| `ZipUtil` | 压缩工具 |
| `CharsetUtil` | 字符编码 |
| `VersionUtil` | 版本比较 |
| `PageUtil` | 分页工具 |
| `CreditCodeUtil` | 社会信用代码 |

### 集合与 Map

| 工具类 | 说明 |
|--------|------|
| `CollUtil` / `ListUtil` | 集合和列表工具 |
| `MapUtil` / `BiMap` | Map 工具和双向 Map |

### 其他核心工具

| 工具类 | 说明 |
|--------|------|
| `DateUtil` / `DateTime` | 日期时间工具（基于 pendulum） |
| `BeanUtil` | Bean 工具 |
| `Base64` / `Base32` | 编解码 |
| `UnicodeUtil` / `CsvUtil` / `StrBuilder` | 文本操作 |
| `NetUtil` / `Ipv4Util` | 网络工具 |
| `MathUtil` | 数学工具 |
| `TreeUtil` | 树结构工具 |
| `FileUtil` / `IoUtil` / `PathUtil` | IO 工具 |

```{toctree}
:hidden:
:maxdepth: 2
:caption: 工具类

str_util
number_util
array_util
object_util
boolean_util
random_util
id_util
hex_util
hash_util
re_util
escape_util
url_util
xml_util
desensitized_util
idcard_util
phone_util
coordinate_util
zip_util
charset_util
version_util
page_util
credit_code_util
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: 集合与 Map

coll
map
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: 日期与编码

date
bean
codec
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: 文本与网络

text
net
math_util
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: 结构与 IO

tree
io
```
```
