# SQL 工具 - SqlUtil

## 由来

在日常开发中，手动拼接 SQL 语句容易出错且代码冗长。`SqlUtil` 提供了常用的 SQL 语句生成方法，支持 SELECT、INSERT、UPDATE、DELETE 以及备份表创建。支持 MySQL、PostgreSQL、SQLite 三种方言。

## 方言支持

所有方法均接受 `dialect` 参数，可选值为 `"mysql"`（默认）、`"postgresql"`、`"sqlite"`。

| 特性 | MySQL | PostgreSQL | SQLite |
|------|-------|------------|--------|
| 标识符引用 | `` `name` `` | `"name"` | `` `name` `` |
| 分页 | `LIMIT offset, count` | `LIMIT count OFFSET offset` | `LIMIT count OFFSET offset` |
| REPLACE INTO | `REPLACE INTO` | `ON CONFLICT DO UPDATE SET` | `INSERT OR REPLACE INTO` |
| INSERT IGNORE | `INSERT ignore INTO` | `ON CONFLICT DO NOTHING` | `INSERT OR IGNORE INTO` |
| ON DUPLICATE KEY | `ON DUPLICATE KEY UPDATE` | `ON CONFLICT DO UPDATE SET` | `ON CONFLICT DO UPDATE SET` |
| VALUES 引用 | `VALUES(col)` | `EXCLUDED.col` | `excluded.col` |

## 方法

### 生成查询 SQL

```python
from hutool import SqlUtil

# MySQL（默认）
SqlUtil.make_select_sql('user', ['name', 'age'])
# 'SELECT `name`,`age` FROM `user`'

# 带条件和排序
SqlUtil.make_select_sql('user', '*', condition='age > 18', order_by=['id'])
# 'SELECT * FROM `user` WHERE age > 18 ORDER BY `id`'

# 分页查询
SqlUtil.make_select_sql('user', '*', page_no=2, page_size=10)
# 'SELECT * FROM `user` LIMIT 10, 10'

# PostgreSQL
SqlUtil.make_select_sql('user', '*', page_no=2, page_size=10, dialect='postgresql')
# 'SELECT * FROM "user" LIMIT 10 OFFSET 10'

# SQLite
SqlUtil.make_select_sql('user', ['name', 'age'], dialect='sqlite')
# 'SELECT `name`,`age` FROM `user`'
```

### 生成插入 SQL

```python
# 单条插入（MySQL）
SqlUtil.make_insert_sql('user', {'name': 'Alice', 'age': 20})

# 批量插入
data = [{'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 30}]
SqlUtil.make_insert_sql('user', data)

# INSERT IGNORE（MySQL）
SqlUtil.make_insert_sql('user', {'name': 'Alice'}, insert_ignore=True)

# INSERT IGNORE（PostgreSQL → ON CONFLICT DO NOTHING）
SqlUtil.make_insert_sql('user', {'name': 'Alice'}, insert_ignore=True, dialect='postgresql')

# INSERT IGNORE（SQLite → INSERT OR IGNORE）
SqlUtil.make_insert_sql('user', {'name': 'Alice'}, insert_ignore=True, dialect='sqlite')

# REPLACE INTO（MySQL）
SqlUtil.make_insert_sql('user', {'name': 'Alice'}, auto_update=True)

# ON DUPLICATE KEY UPDATE（MySQL）
SqlUtil.make_insert_sql('user', {'name': 'Alice', 'age': 20}, update_columns=('name',))

# ON CONFLICT DO UPDATE SET（PostgreSQL，需指定 on_conflict）
SqlUtil.make_insert_sql(
    'user', {'name': 'Alice', 'age': 20},
    update_columns=('name',), on_conflict=('id',), dialect='postgresql'
)

# ON CONFLICT DO UPDATE SET（SQLite）
SqlUtil.make_insert_sql(
    'user', {'name': 'Alice', 'age': 20},
    update_columns=('name',), on_conflict=('id',), dialect='sqlite'
)
```

### 生成更新 SQL

```python
# MySQL
SqlUtil.make_update_sql('user', {'name': 'Bob'}, 'id = 1')
# "UPDATE `user` SET `name`='Bob' WHERE id = 1;\n"

# PostgreSQL
SqlUtil.make_update_sql('user', {'name': 'Bob'}, 'id = 1', dialect='postgresql')
# 'UPDATE "user" SET "name"=\'Bob\' WHERE id = 1;\n'
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

## 链式调用 API

除了上述静态方法，`SqlUtil` 还提供了链式调用 API，通过 `SqlUtil.select()`、`SqlUtil.insert()` 等工厂方法创建 Builder 实例，配合 `Q`（条件组合）、`F`（字段引用）、`ColumnType`（列类型枚举）可以链式生成复杂 SQL 语句。

### Q — 条件组合器

`Q` 支持 `AND(&)`、`OR(|)`、`NOT(~)` 组合条件。

```python
from hutool import SqlUtil, Q

# 简单条件
Q(name='Alice')  # → `name`='Alice'

# OR
Q(age__gt=18) | Q(role='admin')
# → (`age`>18 OR `role`='admin')

# AND（显式）
Q(status='active') & Q(dept='IT')
# → `status`='active' AND `dept`='IT'

# NOT
~Q(status='deleted')
# → NOT `status`='deleted'

# 复杂嵌套
condition = (Q(age__gte=18, status='active') | Q(role='admin')) & Q(dept__in=['IT', 'HR'])
```

**支持的操作符：** `__gt`、`__gte`、`__lt`、`__lte`、`__ne`、`__in`、`__not_in`、`__between`、`__like`、`__contains`、`__startswith`、`__endswith`、`__isnull`

### F — 字段引用

`F` 用于字段间比较、算术运算和聚合函数。

```python
from hutool import SqlUtil, F

# 算术运算
F('balance') + 100   # → `balance`+100
F('stock') - 10      # → `stock`-10
F('price') * 1.5     # → `price`*1.5

# 聚合函数
F.count('*')    # → COUNT(*)
F.sum('amount') # → SUM(`amount`)
F.avg('score')  # → AVG(`score`)
F.max('price')  # → MAX(`price`)
F.min('price')  # → MIN(`price`)
```

### SELECT 链式查询

```python
from hutool import SqlUtil, Q, F

# 基础查询
sql = (SqlUtil.select('user')
    .columns('id', 'name', 'age')
    .where(age__gt=18, status='active')
    .order_by('-age', 'name')
    .limit(10).offset(20)
    .sql())

# 不指定 columns → SELECT *
sql = SqlUtil.select('user').where(id=1).sql()

# Q 组合条件
sql = (SqlUtil.select('user')
    .where(Q(age__gt=18) | Q(role='admin'))
    .where(~Q(status='deleted'))
    .sql())

# F 字段引用
sql = (SqlUtil.select('product')
    .where(price__gt=F('cost') * 1.5)
    .sql())

# 原始 SQL 片段
sql = (SqlUtil.select('user')
    .where('find_in_set(1, status)', Q(age__gt=18))
    .where_raw('YEAR(created_at) = 2024')
    .sql())

# GROUP BY + HAVING
sql = (SqlUtil.select('order')
    .columns('user_id', 'COUNT(*) AS cnt')
    .group_by('user_id')
    .having(cnt__gt=5)
    .sql())

# DISTINCT
sql = SqlUtil.select('user').columns('city').distinct().sql()

# 分页
sql = SqlUtil.select('user').columns('*').page(2, 10).sql()
```

**方法列表：**

| 方法 | 说明 |
|------|------|
| `.columns(*cols)` | 指定查询列，可传原始 SQL 表达式 |
| `.where(*args, **kwargs)` | 添加条件（Q 对象、原始 SQL、field__op=value） |
| `.where_raw(condition)` | 添加原始 SQL WHERE 条件 |
| `.order_by(*fields)` | 排序，前缀 `-` 表示 DESC |
| `.limit(n)` / `.offset(n)` | 分页 |
| `.page(page_no, page_size)` | 按页码分页 |
| `.distinct()` | 去重 |
| `.group_by(*fields)` | 分组 |
| `.having(*args, **kwargs)` | HAVING 条件 |

### INSERT 链式插入

```python
# 基础插入
sql = SqlUtil.insert('user').values(name='Alice', age=20).sql()

# 批量插入
data = [{'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 30}]
sql = SqlUtil.insert('user').values_list(data).sql()

# INSERT IGNORE
sql = SqlUtil.insert('user').values(name='Alice').ignore().sql()

# REPLACE INTO
sql = SqlUtil.insert('user').values(name='Alice').replace().sql()

# ON DUPLICATE KEY UPDATE（MySQL）
sql = (SqlUtil.insert('user')
    .values(name='Alice', age=20)
    .do_update('name')
    .sql())

# ON CONFLICT DO UPDATE SET（PostgreSQL）
sql = (SqlUtil.insert('user', dialect='postgresql')
    .values(name='Alice', age=20)
    .on_conflict('id')
    .do_update('name', 'age')
    .sql())

# ON CONFLICT DO NOTHING
sql = (SqlUtil.insert('user', dialect='postgresql')
    .values(name='Alice')
    .do_nothing()
    .sql())
```

### UPDATE 链式更新

```python
# 基础更新
sql = SqlUtil.update('user').set(name='Bob', age=30).where(id=1).sql()

# F 字段引用
sql = (SqlUtil.update('account')
    .set(balance=F('balance') + 100)
    .where(id=1)
    .sql())

# 原始 SET
sql = (SqlUtil.update('account')
    .set_raw('balance = balance + 100', 'login_count = login_count + 1')
    .where(id=1)
    .sql())

# Q 条件
sql = (SqlUtil.update('user')
    .set(active=False)
    .where(Q(status='banned') | Q(inactive_days__gt=365))
    .sql())
```

### DELETE 链式删除

```python
# 基础删除
sql = SqlUtil.delete('user').where(id=1).sql()

# 多条件
sql = (SqlUtil.delete('user')
    .where(status='inactive', created_at__lt='2020-01-01')
    .sql())

# Q 条件
sql = (SqlUtil.delete('user')
    .where(Q(age__lt=18) | Q(status='banned'))
    .sql())

# 原始 SQL
sql = SqlUtil.delete('user').where_raw('DATEDIFF(NOW(), created_at) > 365').sql()
```

### CREATE TABLE 链式建表

使用 `ColumnType` 枚举自动适配不同方言的列类型。

```python
from hutool import SqlUtil
from hutool.core.sql import ColumnType as CT

# MySQL
sql = (SqlUtil.create_table('user')
    .column('id', CT.SERIAL, primary_key=True)
    .column('name', CT.VARCHAR, type_args='(100)', nullable=False)
    .column('age', CT.INT, default=0)
    .column('bio', CT.TEXT)
    .column('active', CT.BOOLEAN, default=True)
    .column('extra', CT.JSON)
    .if_not_exists()
    .engine('InnoDB')
    .charset('utf8mb4')
    .sql())

# PostgreSQL
sql = (SqlUtil.create_table('user', dialect='postgresql')
    .column('id', CT.SERIAL, primary_key=True)
    .column('name', CT.VARCHAR, type_args='(100)', nullable=False)
    .column('uid', CT.UUID)
    .if_not_exists()
    .sql())

# 复合主键
sql = (SqlUtil.create_table('user_role')
    .column('user_id', CT.INT)
    .column('role_id', CT.INT)
    .primary_key('user_id', 'role_id')
    .sql())
```

**ColumnType 枚举值：**

| 类型 | MySQL | PostgreSQL | SQLite |
|------|-------|------------|--------|
| `SERIAL` | `INT AUTO_INCREMENT` | `SERIAL` | `INTEGER` |
| `BIG_SERIAL` | `BIGINT AUTO_INCREMENT` | `BIGSERIAL` | `INTEGER` |
| `INT` | `INT` | `INTEGER` | `INTEGER` |
| `VARCHAR` | `VARCHAR` | `VARCHAR` | `TEXT` |
| `TEXT` | `TEXT` | `TEXT` | `TEXT` |
| `BOOLEAN` | `TINYINT(1)` | `BOOLEAN` | `INTEGER` |
| `JSON` | `JSON` | `JSONB` | `TEXT` |
| `JSONB` | `JSON` | `JSONB` | `TEXT` |
| `UUID` | `CHAR(36)` | `UUID` | `TEXT` |
| `DATETIME` | `DATETIME` | `TIMESTAMP` | `TEXT` |
| `BLOB` | `BLOB` | `BYTEA` | `BLOB` |
| `DECIMAL` | `DECIMAL` | `DECIMAL` | `NUMERIC` |

```{note}
`ColumnType.VARCHAR`、`ColumnType.CHAR`、`ColumnType.DECIMAL` 等需要参数的类型，通过 `.column(name, CT.VARCHAR, type_args='(255)')` 传入参数。
```
