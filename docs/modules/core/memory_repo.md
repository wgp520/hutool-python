# 内存数据仓库 - MemoryRepo

## 由来

在不需要数据库的场景下（如单元测试、数据处理中间态），需要对内存中的对象集合进行过滤、排序、查询。`MemoryRepo` 提供类 Django ORM 的链式查询接口。

## 基本用法

```python
from hutool import MemoryRepo

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

repo = MemoryRepo([
    User("Alice", 30),
    User("Bob", 25),
    User("Charlie", 35),
])
```

## 方法

### 链式查询

```python
# 过滤（支持 Django 风格查询谓词）
result = repo.filter(age__gte=30)
for user in result:
    print(user.name)  # Alice, Charlie

# 排除（与 filter 相反）
result = repo.exclude(age__gte=30)
for user in result:
    print(user.name)  # Bob

# 排序（- 前缀表示降序）
result = repo.order_by("-age")
for user in result:
    print(user.name)  # Charlie, Alice, Bob
```

### 查询谓词

| 谓词 | 说明 | 示例 |
| --- | --- | --- |
| `gt` / `gte` | 大于 / 大于等于 | `age__gt=18` |
| `lt` / `lte` | 小于 / 小于等于 | `age__lte=30` |
| `contains` / `icontains` | 包含 / 包含（忽略大小写） | `name__contains="li"` |
| `startswith` / `istartswith` | 前缀匹配 | `name__startswith="A"` |
| `endswith` / `iendswith` | 后缀匹配 | `name__endswith="e"` |
| `in` / `not_in` | 在列表中 / 不在列表中 | `age__in=[25, 30]` |
| `not_equal_to` | 不等于 | `age__not_equal_to=0` |
| `range` | 范围 | `age__range=(20, 30)` |

### 获取记录

```python
# 获取唯一记录（多条或零条抛异常）
bob = repo.get(name="Bob")

# 获取第一条匹配（无匹配返回 None）
user = repo.find_first(name="Alice")

# 获取首/末条
first = repo.first()
last = repo.last()
```

### 统计

```python
repo.count()    # 3
repo.exists()   # True
len(repo)       # 3
```

### 转换

```python
# 转为字典
repo.as_dict("name")
# {"Alice": <User>, "Bob": <User>, "Charlie": <User>}
```

---

```{note}
更多方法请参阅 {doc}`API 参考 </apidocs/index>` 文档。
```
