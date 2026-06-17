# SQL 工具 - SqlUtil

## 由来

在日常开发中，手动拼接 SQL 语句容易出错且代码冗长。`SqlUtil` 提供了常用的 SQL 语句生成方法，支持 SELECT、INSERT、UPDATE、DELETE 以及备份表创建。

## 方法

### 生成查询 SQL

```python
from hutool import SqlUtil

# 基础查询
SqlUtil.make_select_sql('user', ['name', 'age'])
# 'SELECT `name`,`age` FROM `user`'

# 带条件和排序
SqlUtil.make_select_sql('user', '*', condition='age > 18', order_by=['id'])
# 'SELECT * FROM `user` WHERE age > 18 ORDER BY `id`'

# 分页查询
SqlUtil.make_select_sql('user', '*', page_no=2, page_size=10)
# 'SELECT * FROM `user` LIMIT 10, 10'
```

### 生成插入 SQL

```python
# 单条插入
SqlUtil.make_insert_sql('user', {'name': 'Alice', 'age': 20})

# 批量插入
data = [{'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 30}]
SqlUtil.make_insert_sql('user', data)

# INSERT IGNORE
SqlUtil.make_insert_sql('user', {'name': 'Alice'}, insert_ignore=True)

# REPLACE INTO（完全覆盖）
SqlUtil.make_insert_sql('user', {'name': 'Alice'}, auto_update=True)

# ON DUPLICATE KEY UPDATE（指定列）
SqlUtil.make_insert_sql('user', {'name': 'Alice', 'age': 20}, update_columns=('name',))
```

### 生成更新 SQL

```python
SqlUtil.make_update_sql('user', {'name': 'Bob'}, 'id = 1')
# "UPDATE `user` SET `name`='Bob' WHERE id = 1;\n"
```

### 生成删除 SQL

```python
SqlUtil.make_delete_sql('user', 'id = 1')
# 'DELETE FROM user WHERE id = 1'
```

### 创建备份表

```python
# 使用默认日期
SqlUtil.create_bak_table_sql('user')
# 'create table user_20240115 as select * from user;\n'

# 指定日期
SqlUtil.create_bak_table_sql('user', bak_date='20240101')
# 'create table user_20240101 as select * from user;\n'

# 批量备份
SqlUtil.create_bak_table_sql(['t1', 't2'], bak_date='20240101')
```

### 值格式化

`SqlUtil._format_sql_value` 内部方法支持自动格式化以下类型：

| 类型 | 转换 |
| ------ | ------ |
| `str`（含 `select`） | 用 `${}` 包裹为子查询 |
| `list` / `dict` | 转为 JSON 字符串 |
| `datetime.datetime` | `%Y-%m-%d %H:%M:%S` |
| `datetime.date` | `%Y-%m-%d` |
| `datetime.time` | `%H:%M:%S` |
| `bool` | `0` / `1` |
| numpy 浮点类型 | `float()` |
| numpy 整数类型 | `int()` |

```{note}
numpy 支持是可选的。安装了 numpy 时会自动识别 `np.float16/32/64`、`np.int8/16/32/64` 等类型并转为 Python 原生类型；未安装 numpy 时完全不影响使用。
```
