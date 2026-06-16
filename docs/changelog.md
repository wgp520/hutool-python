# 更新日志

## v1.1.0 (2026-06-16)

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
- **`Base64Util`** - Base64 编解码工具（URL Safe、无填充、文件/流编码）
- **`Base32Util`** - Base32 编解码工具（含 Extended Hex 字母表）
- **`WeakCache`** - 弱引用缓存（支持弱引用自动清理，不支持弱引用的类型回退到强引用）
- **`CircleCaptcha`** - 圆干扰验证码（在图片上绘制随机圆圈干扰）

#### 核心模块补漏

- **`Ipv4Util`**：
  - IP/Long 互转：`ipv4_to_long`、`long_to_ipv4`（含完整校验）
  - CIDR 操作：`get_begin_ip_str/long`、`get_end_ip_str/long`、`list`（列出范围内 IP）
  - 子网掩码：`count_by_mask_bit`、`get_mask_by_mask_bit`、`is_mask_valid`、`is_mask_bit_valid`、`get_mask_bit`
  - IP 匹配：`is_inner_ip`（含 127.x 回环）、`matches`（通配符匹配）、`format_ip_block`
- **`NetUtil`**：
  - IPv6：`ipv6_to_big_integer`、`big_integer_to_ipv6`、`local_ipv6s`
  - 端口：`get_usable_local_ports`
  - IP 操作：`hide_ip_part_from_long`、`to_ip_list`（CIDR/范围/单 IP）、`local_ips`
  - 工具：`get_localhost_str`、`idn_to_ascii`、`is_unknown`、`ping`、`parse_cookies`、`get_dns_info`、`net_cat`
- **`BeanUtil`**：
  - 字段检测：`has_setter`、`has_getter`、`has_public_field`
  - 动态 Bean：`create_dyna_bean`、`get_bean_desc`
  - 属性操作：`get_property`、`set_property`
  - 映射：`map_to_bean_ignore_case`、`to_bean_ignore_error`、`to_bean_ignore_case`
  - 高级：`bean_to_map_enhanced`（驼峰/下划线+忽略 null）、`copy_properties_with_options`
  - 比较：`is_match_name`、`is_common_fields_equal`、`has_null_field_with_ignore`、`get_field_names`、`edit`
- **`CollUtil`**：`union_all`、`distinct_by`、`find_one_by_field`、`sort_by_pinyin`、`unmodifiable`、`trans`
- **`ListUtil`**：`to_linked_list`、`sort_by_pinyin`、`swap_to`、`swap_element`、`unmodifiable`
- **`IterUtil`**：`to_list_map`、`filtered`、`empty`、`trans`、`clear`
- **`MapUtil`**：`new_tree_map`、`new_identity_map`、`new_concurrent_hash_map`、`wrap`、`unmodifiable`、`get_short`、`get_char`、`empty`
- **`EnumUtil`**：`clear_cache`、`to_string`、`get_enum_at`、`like_value_of`、`get_field_by`、`not_contains`、`equals_ignore_case`
- **`IdcardUtil`**：`convert_18_to_15`、`is_valid_tw_card`、`is_valid_hk_card`、`get_birth_date`、`get_city_code`、`get_district_code`、`get_idcard_info`
- **`CoordinateUtil`**：`out_of_china`、`wgs84_to_mercator`、`mercator_to_wgs84`
- **`XmlUtil`**：`element_text`、`clean_comment`、`append_child`、`append_text`、`is_element`、`to_str`（增强版）、`to_file`、`write`、`create_document`
- **`UnicodeUtil`**：`to_string`、`to_unicode_string`

#### 外部模块补全

- **`DigestUtil`**：
  - 文件摘要：`md5_from_file`、`sha256_from_file`
  - 工厂方法：`digest`、`digest_hex`、`hmac`、`hmac_hex`
  - 其他：`md5_hex_to_16`、`bcrypt`、`bcrypt_check`
- **`SecureUtil`**：
  - 密钥生成：`generate_key`（对称）、`desede`（TripleDES）
  - 便捷摘要：`md5`、`sha1`、`sha256`
  - 便捷 HMAC：`hmac_md5`、`hmac_sha1`、`hmac_sha256`
  - 其他：`pbkdf2`、`decode`（自动 Hex/Base64 检测）、`sign_params`
- **`SignUtil`**：`sign_params_md5`、`sign_params_sha1`、`sign_params_sha256`、`sign_params_hmac_md5`、`sign_params_hmac_sha1`、`sign_params_hmac_sha256`
- **`HttpUtil`**：`download`、`encode_params`、`get_mime_type`、`build_basic_auth`、`normalize_params`
- **`HttpRequest`**：
  - HTTP 方法工厂：`head`、`put`、`patch`、`delete`、`trace`、`options`
  - 链式设置：`content_type`、`keep_alive`、`basic_auth`、`bearer_auth`、`body_bytes`、`params`、`form_file`
- **`HttpResponse`**：`content_encoding`、`is_gzip`、`is_deflate`、`is_chunked`、`get_cookie_str`、`get_cookies`、`get_cookie_value`、`body_bytes`、`write_body`、`get_filename_from_disposition`
- **`HtmlUtil`**：`clean_empty_tag`、`remove_html_tag_by_name`、`unwrap_html_tag`、`remove_html_attr`、`remove_all_html_attr`
- **`JSONUtil`**：`quote`、`escape`、`is_null`、`xml_to_json`、`to_json_bytes`、`wrap`、`get_str`、`get_int`、`get_float`、`get_bool`、`get_list`
- **`WeakCache`**：`get`、`put`、`remove`、`clear`、`size`、`is_empty`、`get_hit_count`、`get_miss_count`、`key_set`
- **`CaptchaUtil`**：新增 `create_circle_captcha` 工厂方法；`LineCaptcha`/`ArithmeticCaptcha` 新增 `get_image_base64`、`write`
- **`SensitiveUtil`**：`is_inited`、`set_char_filter`、`contains_sensitive`（支持 str/list/dict）、`get_found_first_sensitive`、`get_found_all_sensitive`、`init_from_delimited`
- **`PinyinUtil`**：`get_pinyin_char`、`get_first_letter`、`is_chinese`、`get_pinyin_with_tone`
- **`EmojiUtil`**：`is_emoji`、`extract_emojis`、`to_alias`、`to_html`
- **`QrCodeUtil`**：`generate_as_base64`、`generate_as_svg`、`decode`
- **`CronUtil`**：`schedule_with_id`、`remove`、`get_task_count`、`clear`、`matched_dates`
- **`JWTUtil`**：`create_token_with_expire`、`parse_header`、`is_expired`、`get_claim`、`generate_key`、`create_token_with_claims`
- **`SettingUtil`**：`store`、`to_dict`、`create`、`set_value`、`get_group`
- **`PropsUtil`**：`create`、`store`、`to_dict`
- **`YamlUtil`**：`dump_to`、`load_as_dict`、`load_as_list`

#### 现有工具类扩展

- **`StrUtil`**：
  - 比较与判断：`equals_any`、`equals_any_ignore_case`、`equals_char_at`、`contains_only`、`has_letter`、`is_sub_equals`、`is_surround`、`is_wrap`、`is_lower_case`、`is_upper_case`、`is_all_char_match`
  - 公共前缀/后缀：`common_prefix`、`common_suffix`、`compare`、`compare_ignore_case`、`concat`
  - 截取与格式化：`brief`、`max_length`、`fix_length`、`hide`、`move`、`normalize`、`total_length`、`indexed_format`
  - 包裹与填充：`wrap`、`wrap_if_missing`、`wrap_all`、`wrap_all_if_missing`、`pad_after`、`pad_pre`、`repeat_by_length`
  - 替换与移除：`replace_ignore_case`、`replace_last`、`remove_all_prefix`、`remove_all_suffix`、`remove_suf_and_lower_first`
  - 分割与转换：`split_trim`、`strip_all`、`swap_case`、`to_symbol_case`、`trim_to_null`
  - 空值处理与杂项：`empty_if_null`、`desensitized`、`compare_version`
  - 其他：`only_digits`、`de_umlaut`、`full_to_half_width`、`half_to_full_width`、`levenshtein_distance`、`filter_chinese`、`filter_chinese_punctuations`、`left_space_count`、`find_all_indices`
- **`NumberUtil`**：
  - 校验与解析：`is_number`、`is_integer`、`is_double`、`parse_number`、`parse_long`
  - 生成与范围：`range_`、`append_range`、`generate_by_set`
  - 运算：`calculate`（安全数学表达式计算）、`sqrt`
  - 其他：`int_or_default`、`float_or_default`、`avg`、`median`、`num_encode`、`num_decode`、`bytes_to_int`、`int_to_bytes`
- **`BooleanUtil`**：
  - 转换：`to_boolean`、`to_boolean_object`、`is_boolean`、`to_string_true_false`、`to_string_yes_no`、`to_string_on_off`
  - 逻辑运算：`xor_of_wrap`、`exactly_one_true`
  - 三元：`if_true`
- **`RandomUtil`**：
  - `random_chinese`（随机中文字符）、`random_char`、`random_day`、`random_ints`
  - `random_string_without_str`、`random_string_lower_without_str`（排除指定字符）
  - `random_element_weighted`（加权随机别名）、`random_ele_with_condition`（条件随机选取）
  - 其他：`weighted_choice`
- **`ReUtil`**：
  - 查找：`find_all`、`find_all_group0`、`find_all_group1`、`find_first_number`
  - 位置：`index_of`、`last_index_of`
  - 删除/提取：`del_first`、`del_last`、`del_pre`、`extract_multi_and_del_pre`
- **`HexUtil`**：
  - `is_hex_number`（是否十六进制数）、`to_unicode_hex`（字符→`\uXXXX`）
- **`URLUtil`**：
  - `build_query`（字典→查询字符串）、`encode_blank`（编码空格）、`complete_url`（补全相对URL）、`get_params`（解析URL参数为字典）
- **`DateUtil`**：
  - 判断：`is_last_day_of_month`、`is_expired`、`is_overlap`、`is_between`、`date_trunc`
  - 属性：`day_of_year`、`length_of_month`、`length_of_year`、`millisecond`、`get_zodiac`、`get_chinese_zodiac`、`get_week`
  - 时间跨度：`get_monthspan`、`get_weekspan`、`get_quarterspan`、`get_yearspan`
  - 操作与转换：`compare`、`convert_timezone`、`format_chinese_date`、`month_add`、`convert_to_date`、`convert_to_datetime`、`age_by_birthday`
  - RFC 格式：`rfc3339_date`、`rfc3339_date_parse`、`rfc2616_date`、`rfc2616_date_parse`
  - 实用：`is_same_month`、`is_same_week`、`time_ago`、`iso_timestamp`、`format_between`、`between_day`
- **`BeanUtil`**：
  - `is_bean`（是否为Bean）、`is_empty`、`is_not_empty`、`has_null_field`
  - `desc_for_each`（遍历字段应用函数）、`fill_bean`（默认值填充None字段）
- **`NetUtil`**：
  - `is_inner_ip`（是否内网IP）、`is_in_range`（IP是否在CIDR范围内）、`hide_ip_part`（遮蔽IP）
  - `local_ipv4s`（本机IPv4列表）、`get_local_host_name`（主机名）、`get_ip_by_host`（解析主机名）、`to_absolute_url`（补全相对URL）
- **`IdcardUtil`**：
  - `get_year_by_id_card`（提取出生年）、`get_month_by_id_card`（提取出生月）、`get_day_by_id_card`（提取出生日）
- **`PhoneUtil`**：
  - `is_mobile_simple`（宽松手机号判断：11位数字，1开头）
- **`CharsetUtil`**：
  - `clean_invalid`（清除无效控制字符，保留\t\n\r）
- **`CollUtil`**：
  - `is_sub`（子集判断）、`intersection`（交集）、`disjunction`（对称差集）
  - `safe_min`、`safe_max`
- **`IdUtil`**：
  - `unique_machine_id`（机器唯一ID）、`guid128`（26字符全局唯一ID）
- **`EscapeUtil`**：
  - `unescape_html_chars`（HTML 实体反转义）
- **`SecureUtil`**：
  - `caesar_encode`、`caesar_decode`（凯撒密码加解密）
- **`JSONUtil`**：
  - `map_dict_keys`（递归映射键名）、`map_list_keys`（列表字典键名映射）
  - `convert_keys_to_camel`（snake→camel）、`convert_keys_to_snake`（camel→snake）
- **`CheckUtil`**：
  - `is_mac`（MAC地址）、`is_chinese`（全中文）、`is_english`（全英文字母）、`is_symbol`（全符号）
  - `contains_url`（包含URL）、`is_blank_line`（空白行）、`is_qq`（QQ号）、`is_date_time`（日期时间格式）、`is_post_code`（邮编）
- **`FileUtil`**：
  - `tail`（读取文件最后N行）
- **`MapUtil`**：
  - `top_n_keys`（取值最大的前N个键）、`to_map_list`（列表转Map，值为列表）

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
