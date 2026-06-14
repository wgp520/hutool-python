# 快速开始

本文档将带你快速了解 Hutool-Python 的核心功能。每个模块都提供了简单易用的静态方法，无需创建实例即可调用。

## 字符串工具 - StrUtil

```python
from hutool import StrUtil

# 判空
StrUtil.is_empty(None)       # True
StrUtil.is_blank("  \t\n")   # True
StrUtil.has_blank("abc", "") # True

# 子串
StrUtil.sub("abcdefgh", 2, 5)   # "cde"
StrUtil.sub_before("abc.def", ".")  # "abc"
StrUtil.sub_after("abc.def", ".")   # "def"
StrUtil.sub_between("aaBBcc", "BB") # ""

# 格式化（类似 slf4j）
StrUtil.format("{}爱{}，就像老鼠爱大米", "我", "你")
# "我爱你，就像老鼠爱大米"

# 命名转换
StrUtil.to_camel_case("hello_world")  # "helloWorld"
StrUtil.to_snake_case("helloWorld")   # "hello_world"

# 填充与重复
StrUtil.pad("abc", 6, "0")       # "abc000"
StrUtil.center("abc", 7, "*")    # "**abc**"
StrUtil.repeat("ab", 3)          # "ababab"
```

## 数字工具 - NumberUtil

```python
from hutool import NumberUtil

# 精确运算
NumberUtil.add(0.1, 0.2)       # Decimal('0.3')
NumberUtil.div(10, 3, 2)       # Decimal('3.33')

# 判断
NumberUtil.is_number("123.45") # True
NumberUtil.is_int("123")       # True
NumberUtil.is_odd(3)           # True

# 格式化
NumberUtil.decimal_format("#,##0.00", 1234567.89)  # "1,234,567.89"
```

## 日期工具 - DateUtil

```python
from hutool import DateUtil, DateTime

# 获取当前时间
DateUtil.now()                   # "2024-01-01 12:00:00"
DateUtil.today()                 # "2024-01-01"

# 解析
dt = DateUtil.parse("2024-01-01")
dt = DateUtil.parse("20240101", "yyyyMMdd")

# 格式化
DateUtil.format(dt, "yyyy/MM/dd")  # "2024/01/01"

# 日期偏移
tomorrow = DateUtil.tomorrow()
next_month = DateUtil.offset_month(dt, 1)

# 时间差
days = DateUtil.between_day(start, end)
DateUtil.format_between(start, end)  # "3天2小时5分"
```

## 集合工具 - CollUtil

```python
from hutool import CollUtil

# 判空
CollUtil.is_empty([])      # True
CollUtil.is_not_empty([1]) # True

# 分组与分区
items = [1, 2, 3, 4, 5]
CollUtil.partition(items, 2)  # [[1, 2], [3, 4], [5]]

# 转换
CollUtil.join([1, 2, 3], ",")  # "1,2,3"
CollUtil.distinct([1, 2, 2, 3])  # [1, 2, 3]

# 查找
CollUtil.find_first([1, 2, 3], lambda x: x > 1)  # 2
CollUtil.any_match([1, 2, 3], lambda x: x > 2)    # True
```

## HTTP 客户端 - HttpUtil

```python
from hutool import HttpUtil

# GET 请求
content = HttpUtil.get("https://httpbin.org/get")

# POST 请求
result = HttpUtil.post("https://httpbin.org/post",
                       json_data={"key": "value"})

# 链式请求
from hutool import HttpRequest

response = (HttpRequest.get("https://httpbin.org/get")
    .header("Accept", "application/json")
    .timeout(5000)
    .execute())

print(response.body)
print(response.status)
```

## 加密工具

```python
from hutool import DigestUtil
from hutool import SecureUtil

# 摘要
DigestUtil.md5_hex("hello")          # MD5 哈希
DigestUtil.sha256_hex("hello")       # SHA-256 哈希
DigestUtil.hmac_sha256_hex("hello", "key")  # HMAC

# AES 加密
key = SecureUtil.generate_aes_key(128)
encrypted = SecureUtil.encrypt_aes(b"hello", key, "CBC")
decrypted = SecureUtil.decrypt_aes(encrypted, key, "CBC")
```

## JSON 工具 - JSONUtil

```python
from hutool import JSONUtil

# 序列化
json_str = JSONUtil.to_json_str({"name": "test", "value": 123})
pretty = JSONUtil.to_json_pretty_str({"name": "test"})

# 解析
obj = JSONUtil.parse_obj('{"name": "test"}')
arr = JSONUtil.parse_array('[1, 2, 3]')

# 路径查询
data = {"user": {"name": "张三", "age": 25}}
name = JSONUtil.get_by_path(data, "user.name")  # "张三"
```

## 缓存

```python
from hutool import CacheUtil

# LRU 缓存
cache = CacheUtil.new_lru_cache(capacity=100)
cache.put("key", "value")
value = cache.get("key")  # "value"

# 定时缓存（5秒过期）
timed = CacheUtil.new_timed_cache(timeout=5)
timed.put("temp", "data")
```

## ID 生成 - IdUtil

```python
from hutool import IdUtil

IdUtil.random_uuid()     # "a1b2c3d4-e5f6-..."
IdUtil.simple_uuid()     # "a1b2c3d4e5f6..."（无横线）
IdUtil.nano_id()         # "V1StGXR8_Z5jdHi6B-myT"
IdUtil.snowflake_id()    # 雪花 ID（整数）
```

## JWT 工具 - JWTUtil

```python
from hutool import JWTUtil

# 生成 Token
token = JWTUtil.create_token(
    {"sub": "1234567890", "name": "test"},
    secret="my-secret"
)

# 解析
payload = JWTUtil.parse_token(token, secret="my-secret")

# 验证
JWTUtil.verify(token, secret="my-secret")  # True
```

## 更多模块

每个模块的详细文档请参阅左侧导航栏的模块文档部分。
