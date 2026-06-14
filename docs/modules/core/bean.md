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
```
