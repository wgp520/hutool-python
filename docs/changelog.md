# 更新日志

## v1.1.0 (2026-06-17)

### 新增

#### 新增工具类

- **`CheckUtil`** - 校验码与格式校验（EAN/Verhoeff 算法、70+ is_*/validate_* 方法）
- **`WorkdayUtil`** - 工作日计算（中国法定节假日，支持自定义假日）
- **`MoneyUtil`** - 货币计算（元/分转换、含税/不含税，Decimal 精确运算）
- **`BankUtil`** - 银行工具（IBAN 计算与验证）
- **`IterUtil`** - 迭代工具（12 个 itertools recipes）
- **`TimingUtil`** - 计时工具（timethis 装饰器 + Timer 上下文管理器）
- **`ExecUtil`** - 并发执行（线程池/进程池批量任务）
- **`ProfUtil`** - 性能分析（cProfile 装饰器 + 上下文管理器）
- **`MemoryRepo`** - 内存数据仓库（类 Django ORM 链式查询）
- **`ConvertUtil`** - 类型转换（bytes↔int、通用类型转换、中英文数字互转）
- **`ColorUtil`** - 颜色工具（hex↔rgb）
- **`ImageUtil`** - 图片工具（魔数格式检测、缩放、水印、人脸检测）
- **`UserAgentUtil`** - UA 生成器（Chrome/Firefox/Safari 等随机生成）
- **`Base64Util`** / **`Base32Util`** - 编解码工具
- **`WeakCache`** - 弱引用缓存
- **`CircleCaptcha`** - 圆干扰验证码
- **`Struct`** - 字典子类，支持属性访问（`s.name`）+ `Struct.from_dict` 类方法
- **`SqlUtil`** - SQL 生成工具（SELECT/INSERT/UPDATE/DELETE/备份表，可选 numpy 支持）
- **`CronValidator`** - Cron 表达式校验（Quartz 风格 6-7 字段，逐字段校验 + 整体校验）

#### 现有工具类大幅扩展

- **`StrUtil`**：比较判断、公共前后缀、截取格式化、包裹填充、高级替换、Unicode/CodePoint 操作、编辑距离、全角半角转换等
- **`NumberUtil`**：安全数学运算、解析、生成与范围、动态运算符执行
- **`DateUtil`**：时间跨度、RFC 格式、时区转换、农历生肖、范围生成器等
- **`FileUtil`**：读写、路径操作、状态检测、内容校验（MD5/SHA/CRC32）
- **`CheckUtil`**：邮箱/IP/URL/UUID/手机/车牌/身份证/银行卡等格式校验 + Validator 验证器
- **`BeanUtil`**：字段检测、动态 Bean、属性操作、映射、比较
- **`NetUtil`** / **`Ipv4Util`**：IPv6、CIDR、端口扫描、IP 匹配
- **`CollUtil`** / **`ListUtil`** / **`MapUtil`**：去重、分块、排序、不可修改集合
- **`IoUtil`** / **`PathUtil`** / **`XmlUtil`**：校验、遍历、XPath、字典↔XML 转换
- **`SecureUtil`** / **`DigestUtil`**：对称加密、HMAC、bcrypt、密钥对生成
- **`HttpRequest`** / **`HttpResponse`**：HTTP 方法工厂、链式设置、Cookie 解析
- **`CacheUtil`**：TTL 函数缓存、记忆化装饰器、LRU 缓存、单次执行装饰器
- **`IdUtil`**：机器 ID 生成、Verhoeff ID 构建
- **`ReUtil`**：查找/位置/删除/提取扩展，正则替换回调
- **`JSONUtil`**：键名映射（snake↔camel）、JSON 比较、XML 解析
- 其他：`EnumUtil`、`IdcardUtil`、`CoordinateUtil`、`PhoneUtil`、`CharsetUtil`、`EscapeUtil`、`HexUtil`、`URLUtil`、`EmojiUtil`、`PinyinUtil`、`QrCodeUtil`、`CaptchaUtil`、`JWTUtil`、`CsvUtil` 等均有扩展

## v1.0.1 (2026-06-14)

- 添加文档注释

## v1.0.0 (2026-06-13)

### 首次发布

- 初始版本发布
- 移植 Java Hutool 核心功能至 Python
- 支持 Python >= 3.8

#### 核心工具 (core)

- `StrUtil` - 字符串工具（160+ 方法）
- `NumberUtil` - 数字工具
- `ArrayUtil` - 数组工具
- `ObjectUtil` - 对象工具
- `BooleanUtil` - 布尔工具
- `RandomUtil` - 随机工具
- `IdUtil` - ID 生成（UUID、NanoId、雪花 ID）
- `HexUtil` - 十六进制工具
- `HashUtil` - 哈希算法
- `ReUtil` - 正则工具
- `EscapeUtil` - 转义工具
- `URLUtil` - URL 工具
- `XmlUtil` - XML 工具
- `DesensitizedUtil` - 信息脱敏
- `IdcardUtil` - 身份证工具
- `PhoneUtil` - 手机号工具
- `CoordinateUtil` - 坐标转换
- `ZipUtil` - 压缩工具
- `CharsetUtil` - 字符编码
- `VersionUtil` - 版本比较
- `PageUtil` - 分页工具
- `CreditCodeUtil` - 社会信用代码校验
- `CollUtil` / `ListUtil` - 集合工具
- `MapUtil` / `BiMap` - Map 工具
- `DateUtil` / `DateTime` - 日期工具（基于 pendulum）
- `BeanUtil` - Bean 工具
- `Base64` / `Base32` - 编解码
- `UnicodeUtil` / `CsvUtil` / `StrBuilder` - 文本操作
- `NetUtil` / `Ipv4Util` - 网络工具
- `MathUtil` / `BitStatusUtil` - 数学工具
- `TreeUtil` - 树结构
- `FileUtil` / `IoUtil` / `PathUtil` - IO 工具

#### 外部模块

- `HttpUtil` / `HttpRequest` / `HttpResponse` / `HtmlUtil` - HTTP 客户端（基于 httpx）
- `JSONUtil` - JSON 工具
- `DigestUtil` / `SecureUtil` / `SignUtil` - 加密工具（基于 cryptography）
- `FIFOCache` / `LFUCache` / `LRUCache` / `TimedCache` - 缓存
- `CaptchaUtil` - 验证码（基于 Pillow）
- `SensitiveUtil` - 敏感词过滤（DFA 算法）
- `EmojiUtil` / `PinyinUtil` / `TemplateUtil` / `QrCodeUtil` - 扩展工具
- `CronUtil` / `CronPattern` - 定时任务
- `JWTUtil` - JWT 工具（基于 PyJWT）
- `YamlUtil` / `PropsUtil` - 配置工具
