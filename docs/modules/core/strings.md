# 字符串工具 - StrUtil

## 由来

类似于 Apache Commons Lang 中的 `StringUtil`，使用 `StrUtil` 作为名称是因为更简洁。`Str` 这个简写已经深入人心，大家都明白是字符串的意思。

## 方法

### 判空方法

```python
from hutool import StrUtil

# isEmpty / isNotEmpty —— 判断 null 或 ""
StrUtil.is_empty(None)     # True
StrUtil.is_empty("")       # True
StrUtil.is_empty("abc")    # False

# isBlank / isNotBlank —— 判断 null、"" 或空白字符
StrUtil.is_blank(None)     # True
StrUtil.is_blank("  \t\n") # True
StrUtil.is_blank("abc")    # False

# hasBlank / hasEmpty —— 多个字符串中是否有空
StrUtil.has_blank("abc", "", "def")   # True
StrUtil.has_empty("abc", None, "def") # True

# isAllBlank / isAllEmpty —— 是否全部为空
StrUtil.is_all_blank("", "  ", None)  # True
```

### 子串方法

`sub` 方法比原生切片更安全，支持负数索引且不会越界：

```python
str_val = "abcdefgh"
StrUtil.sub(str_val, 2, 5)    # "cde"
StrUtil.sub(str_val, 2, -3)   # "cde"
StrUtil.sub(str_val, 3, 2)    # ""（自动修正顺序）

# subBefore / sub_after
StrUtil.sub_before("abc.def", ".")      # "abc"
StrUtil.sub_after("abc.def", ".")       # "def"
StrUtil.sub_before("abc.def", ".", True) # "abc"（从最后一个分隔符截取）

# subBetween
StrUtil.sub_between("aaBBccDD", "BB", "DD")  # "cc"
```

### 去前后缀

```python
StrUtil.remove_prefix("pretty_girl.jpg", ".jpg")  # "pretty_girl"
StrUtil.remove_suffix("pretty_girl.jpg", "pretty_")  # "girl.jpg"
StrUtil.remove_prefix_ignore_case("ABCdef", "abc")  # "def"
```

### 格式化

灵感来自 slf4j 的 `{}` 占位符：

```python
StrUtil.format("{}爱{}，就像老鼠爱大米", "我", "你")
# "我爱你，就像老鼠爱大米"
```

### 命名转换

```python
StrUtil.to_camel_case("hello_world")  # "helloWorld"
StrUtil.to_snake_case("helloWorld")   # "hello_world"
StrUtil.to_under_score_case("HelloWorld")  # "hello_world"
```

### 填充与重复

```python
StrUtil.pad("abc", 6, "0")         # "abc000"
StrUtil.center("abc", 7, "*")      # "**abc**"
StrUtil.repeat("ab", 3)            # "ababab"
StrUtil.repeat_and_join(",", 3)    # ",,,"
```

### 分割与连接

```python
StrUtil.split("a,b,c", ",")           # ["a", "b", "c"]
StrUtil.split("a,,b,c", ",", -1, False, True)  # ["a", "b", "c"]（忽略空）

StrUtil.join(",", "a", "b", "c")      # "a,b,c"
StrUtil.join(",", ["a", "b", "c"])    # "a,b,c"
```

### 类型判断

```python
StrUtil.is_numeric("123")      # True
StrUtil.is_number("123.45")    # True
StrUtil.is_alpha("abc")        # True
StrUtil.is_alpha_upper("ABC")  # True
StrUtil.is_alpha_lower("abc")  # True
```

### 统计

```python
StrUtil.count("ababab", "ab")  # 3
StrUtil.count("ababab", "a")   # 3
```

### 替换

```python
StrUtil.replace("aabbcc", "bb", "xx")         # "aaxxcc"
StrUtil.replace_first("aabbcc", "b", "x")      # "axbcc"
StrUtil.replace_chars("aabbcc", "ac", "x")      # "xxbbxx"
```

### 相似度

```python
StrUtil.similar("hello", "hallo")    # 0.8
StrUtil.similar("hello", "hello")    # 1.0
```

### 文本分析

```python
# 计算前导空白（tab 算 4 个空格）
StrUtil.left_space_count("    hello")  # 4
StrUtil.left_space_count("\thello")    # 4
StrUtil.left_space_count("hello")      # 0

# 查找子串所有出现位置
StrUtil.find_all_indices("abcabc", "bc")  # [1, 4]
StrUtil.find_all_indices("hello", "x")    # []
```

### 安全字符串处理

```python
# 提取数字
StrUtil.only_digits("abc123def456")  # "123456"

# 全角/半角转换
StrUtil.full_to_half_width("Ｈｅｌｌｏ")  # "Hello"
StrUtil.half_to_full_width("Hello")        # "Ｈｅｌｌｏ"

# 移除中文字符
StrUtil.filter_chinese("你好World")  # "World"

# 移除中文标点
StrUtil.filter_chinese_punctuations("你好，World！")  # "你好World"

# 德语变音符号转 ASCII
StrUtil.de_umlaut("München")  # "Muenchen"

# Levenshtein 编辑距离
StrUtil.levenshtein_distance("kitten", "sitting")  # 3
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
