# 更新日志

## v1.1.0 (2026-06-15)

### 新增

#### 新增工具类

- **`CheckUtil`** - 校验码计算工具（EAN/UPC 条形码校验位、Verhoeff 校验位算法）
- **`WorkdayUtil`** - 工作日计算工具（中国法定节假日配置，支持自定义假日）
- **`MoneyUtil`** - 货币计算工具（元/分转换、含税/不含税价格计算，基于 Decimal 精确运算）
- **`BankUtil`** - 银行工具（IBAN 计算与验证，ISO 7064 mod 97-10）
- **`IterUtil`** - 迭代工具类（take/tail/nth/all_equal/quantify/flatten/pairwise/grouper/roundrobin/partition/powerset/unique_everseen，12 个 itertools recipes）
- **`TimingUtil`** - 计时工具类（timethis 装饰器 + Timer 上下文管理器）
- **`ExecUtil`** - 并发执行工具类（线程池/进程池批量任务提交）
- **`ProfUtil`** - 性能分析工具类（cProfile 装饰器 + 上下文管理器）
- **`MemoryRepo`** - 内存数据仓库（类 Django ORM 的 filter/exclude/order_by/get 链式查询）
- **`ConvertUtil`** - 类型转换工具类（bytes↔int、通用类型转换、安全字符串转换）
- **`ColorUtil`** - 颜色工具类（hex↔rgb 转换，支持 #RGB/#RRGGBB 格式）
- **`ImageUtil`** - 图片工具类（通过魔数检测图片格式：JPEG/PNG/GIF/BMP/TIFF/WebP）
- **`UserAgentUtil`** - UserAgent 生成器（Chrome/Firefox/Safari/Opera/IE/Edge 浏览器 UA 随机生成）

#### 现有工具类扩展

- **`StrUtil`** +9 方法：
  - `only_digits()`（提取数字）
  - `de_umlaut()`（德语变音符号转 ASCII）
  - `full_to_half_width()`（全角→半角）
  - `half_to_full_width()`（半角→全角）
  - `levenshtein_distance()`（Levenshtein 编辑距离）
  - `filter_chinese()`（移除中文字符）
  - `filter_chinese_punctuations()`（移除中文标点）
  - `left_space_count()`（计算前导空白，tab=4 空格）
  - `find_all_indices()`（查找子串所有出现位置）
- **`NumberUtil`** +8 方法：
  - `int_or_default()`
  - `float_or_default()`（安全类型转换）
  - `avg()`、`median()`（统计聚合）
  - `num_encode()`、`num_decode()`（Base62 编解码）
  - `bytes_to_int()`（bytes 大端序转 int）
  - `int_to_bytes()`（int 大端序转 bytes）
- **`DateUtil`** +18 方法：
  - `date_trunc()`（日期截断）
  - `get_week()`（周号）
  - `get_monthspan()`/`get_weekspan()`/`get_quarterspan()`/`get_yearspan()`（时间跨度）
  - `month_add()`（月份加减）
  - `rfc3339_date()`/`rfc3339_date_parse()`/`rfc2616_date()`/`rfc2616_date_parse()`（RFC 格式化与解析）
  - `convert_to_date()`/`convert_to_datetime()`（通用日期转换）
  - `age_by_birthday()`（根据生日计算年龄）
  - `is_same_month()`（判断同月）
  - `is_same_week()`（判断同周）
  - `time_ago()`（相对时间"3天前"）
  - `iso_timestamp()`（ISO 8601 时间戳）
- **`IdUtil`** +2 方法：
  - `unique_machine_id()`（机器唯一 ID）
  - `guid128()`（26 字符全局唯一 ID）
- **`CollUtil`** +3 方法：
  - `safe_min()`、`safe_max()`（空集合安全返回 None）
  - `find_duplicates()`（查找重复元素）
- **`EscapeUtil`** +1 方法：
  - `unescape_html_chars()`（HTML 实体反转义）
- **`RandomUtil`** +1 方法：
  - `weighted_choice()`（加权随机选择）
- **`SecureUtil`** +2 方法：
  - `caesar_encode()`、`caesar_decode()`（凯撒密码加解密）
- **`JSONUtil`** +4 方法：
  - `map_dict_keys()`（递归映射键名）
  - `map_list_keys()`（列表字典键名映射）
  - `convert_keys_to_camel()`（snake→camel）
  - `convert_keys_to_snake()`（camel→snake）
- **`CheckUtil`** +9 方法：
  - `is_mac()`（MAC 地址校验）
  - `is_chinese()`（全中文校验）
  - `is_english()`（全英文字母校验）
  - `is_symbol()`（全符号校验）
  - `contains_url()`（是否包含 URL）
  - `is_blank_line()`（空白行校验）
  - `is_qq()`（QQ 号校验）
  - `is_date_time()`（日期时间格式校验）
  - `is_post_code()`（邮编校验）
- **`FileUtil`** +1 方法：
  - `tail()`（读取文件最后 N 行）
- **`MapUtil`** +1 方法：
  - `top_n_keys()`（取值最大的前 N 个键）

## v1.0.1 (2026-06-14)

- 添加文档注释

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
