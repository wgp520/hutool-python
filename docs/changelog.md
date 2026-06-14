# 更新日志

## v1.0.0 (2026-06-13)

### 新增

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
