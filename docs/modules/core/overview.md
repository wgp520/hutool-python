# 核心模块概述

`hutool.core` 是 Hutool-Python 的核心模块，提供了最基础、最常用的工具类。

## 模块列表

### 工具类 (core/util/)

| 工具类 | 说明 |
| ------ | ---- |
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
| `CheckUtil` | 校验码计算（EAN/Verhoeff）及格式校验 |
| `ConvertUtil` | 类型转换工具 |
| `ColorUtil` | 颜色格式转换（hex↔rgb） |
| `ImageUtil` | 图片格式检测（魔数识别） |
| `UserAgentUtil` | UserAgent 随机生成器 |
| `Struct` | 结构体（dict 子类，支持属性访问，递归嵌套转换） |

### 集合与 Map

| 工具类 | 说明 |
| ------ | ---- |
| `CollUtil` / `ListUtil` | 集合和列表工具 |
| `MapUtil` / `BiMap` | Map 工具和双向 Map |

### 其他核心工具

| 工具类 | 说明 |
| ------ | ---- |
| `DateUtil` / `DateTime` | 日期时间工具（基于 pendulum） |
| `BeanUtil` | Bean 工具 |
| `Base64` / `Base32` | 编解码 |
| `UnicodeUtil` / `CsvUtil` / `StrBuilder` | 文本操作 |
| `NetUtil` / `Ipv4Util` | 网络工具 |
| `MathUtil` | 数学工具 |
| `TreeUtil` | 树结构工具 |
| `FileUtil` / `IoUtil` / `PathUtil` | IO 工具 |
| `WorkdayUtil` | 工作日计算（中国法定假日） |
| `MoneyUtil` | 货币计算（元/分转换、税价计算） |
| `BankUtil` | 银行工具（IBAN 计算与验证） |
| `IterUtil` | 迭代工具（itertools recipes） |
| `TimingUtil` / `timethis` | 计时工具（装饰器 + Timer） |
| `ExecUtil` | 并发执行（线程池/进程池） |
| `ProfUtil` | 性能分析（cProfile） |
| `MemoryRepo` | 内存数据仓库（链式查询） |
| `TimeThis` / `ProfileDeco` / `CacheFunction` / `Memoize` / `FuncOnce` / `TtlLruCache` / `NoneOnException` | class-based 装饰器（支持有括号/无括号/同步/协程） |

```{toctree}
:hidden:
:maxdepth: 2
:caption: 工具类

strings
number
array
object
boolean
randoms
id
hex
hasher
regex
escape
url
xml
desensitized
idcard
phone
coordinate
zip
charset
version
page
credit_code
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
math
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: 结构与 IO

tree
io
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: v1.1.0 新增

check
workday
money
bank
iter
timing
exec
prof
memory_repo
convert
color
image
user_agent
struct
decorators
sql
```
