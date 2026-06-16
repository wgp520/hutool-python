# Bean 工具 - BeanUtil

## 由来

Java 中 Bean（对象与字典之间的转换）是极其常见的操作。Python 中通过 `BeanUtil` 简化对象与字典之间的互转。

## 方法

```python
from hutool import BeanUtil

# 对象转字典
class User:
    def __init__(self):
        self.name = "张三"
        self.age = 25

user = User()
data = BeanUtil.bean_to_map(user)  # {"name": "张三", "age": 25}

# 字典转对象
user2 = BeanUtil.map_to_bean({"name": "李四", "age": 30}, User)
print(user2.name)  # "李四"

# 属性拷贝
source = User()
target = User()
BeanUtil.copy_properties(source, target)

# 获取/设置字段值
BeanUtil.get_field_value(user, "name")        # "张三"
BeanUtil.set_field_value(user, "name", "李四")

# 批量转换
users = BeanUtil.to_bean_list(
    [{"name": "张三"}, {"name": "李四"}],
    User
)

# 判断是否为 Bean
BeanUtil.is_bean(User())    # True
BeanUtil.is_bean("string")  # False
BeanUtil.is_bean({})        # False

# 判断 Bean 字段是否全为 None
user3 = User()
user3.name = None
user3.age = None
BeanUtil.is_empty(user3)       # True
BeanUtil.is_not_empty(user)    # True（user.name 非 None）

# 判断 Bean 是否有 None 字段
BeanUtil.has_null_field(user3)  # True

# 遍历字段应用函数
result = {}
BeanUtil.desc_for_each({"a": 1, "b": 2}, lambda k, v: result.update({k: v}))
# result = {"a": 1, "b": 2}

# 用默认值填充 None 字段
BeanUtil.fill_bean(user3, lambda key: f"default_{key}")
# user3.name = "default_name", user3.age = "default_age"

# 去除字符串字段首尾空白
BeanUtil.trim_str_fields(user)
# user.name 会被 strip()

# 拷贝为对象列表
users = BeanUtil.copy_to_list([{"name": "a"}, {"name": "b"}], User)
```
