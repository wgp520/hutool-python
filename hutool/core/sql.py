"""SQL 工具类。

提供 SQL 语句的生成工具，支持 SELECT、INSERT、UPDATE、DELETE 以及备份表创建。
支持 MySQL、PostgreSQL、SQLite 三种方言。
值格式化支持 Python 内置类型和可选的 numpy 类型（无需安装 numpy）。

链式调用 API 支持通过 ``SqlUtil.select()`` 等工厂方法创建 Builder 实例，
配合 ``Q``（条件组合）、``F``（字段引用）、``ColumnType``（列类型枚举）
可以链式生成复杂 SQL 语句。
"""

import copy
import datetime
import enum
import json
import re
from typing import Any, Dict, List, Optional, Tuple, Union

# numpy 可选支持：安装了 numpy 时自动识别其数值类型，未安装时零开销
try:
    import numpy as _np

    _NUMPY_FLOAT_TYPES = (_np.float16, _np.float32, _np.float64)
    _NUMPY_INT_TYPES = (_np.int8, _np.int16, _np.int32, _np.int64)
except ImportError:
    _NUMPY_FLOAT_TYPES = ()
    _NUMPY_INT_TYPES = ()

# 支持的方言
_VALID_DIALECTS = ("mysql", "postgresql", "sqlite")


class SqlUtil:
    """SQL 工具类，用于生成常用 SQL 语句。

    支持 MySQL、PostgreSQL、SQLite 三种方言。
    支持 INSERT ON DUPLICATE KEY UPDATE、REPLACE INTO、INSERT IGNORE
    以及分页查询、备份表等常见操作。
    """

    @staticmethod
    def make_select_sql(
        table: str,
        columns: Union[List[str], str],
        condition: Optional[str] = None,
        order_by: Optional[list] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        dialect: str = "mysql",
    ) -> str:
        """生成查询 SQL。

        :param table: 表名
        :param columns: 要查询的字段名，列表或原始字符串
        :param condition: WHERE 条件（不含 WHERE 关键字）
        :param order_by: 排序字段列表
        :param page_no: 页码（从 1 开始）
        :param page_size: 每页记录数
        :param dialect: SQL 方言，支持 ``"mysql"``（默认）、``"postgresql"``、``"sqlite"``
        :return: 查询 SQL 字符串

        ::

            >>> SqlUtil.make_select_sql('user', ['name', 'age'])
            'SELECT `name`,`age` FROM `user`'
            >>> SqlUtil.make_select_sql('user', '*', page_no=2, page_size=10)
            'SELECT * FROM `user` LIMIT 10, 10'
            >>> SqlUtil.make_select_sql('user', '*', page_no=2, page_size=10, dialect='postgresql')
            'SELECT * FROM "user" LIMIT 10 OFFSET 10'
        """
        SqlUtil._validate_dialect(dialect)

        def q(name):
            return SqlUtil._quote(name, dialect)

        if isinstance(columns, list):
            select_columns = ",".join([q(key) for key in columns])
        else:
            select_columns = columns
        sql = f"SELECT {select_columns} FROM {q(table)}"
        if condition:
            sql += f" WHERE {condition}"
        if order_by:
            order_by_columns = ",".join([q(key) for key in order_by])
            sql += f" ORDER BY {order_by_columns}"
        if page_no is not None and page_size is not None:
            page_no = 1 if page_no < 1 else page_no
            limit = (page_no - 1) * page_size
            offset = page_size
            if dialect == "mysql":
                sql += f" LIMIT {limit}, {offset}"
            else:
                sql += f" LIMIT {offset} OFFSET {limit}"
        return sql

    @staticmethod
    def make_insert_sql(
        table: str,
        data: Union[dict, list],
        auto_update: bool = False,
        update_columns: tuple = (),
        update_columns_value: tuple = (),
        insert_ignore: bool = False,
        separator: str = ";\n",
        dialect: str = "mysql",
        on_conflict: Optional[tuple] = None,
    ) -> str:
        """生成插入 SQL。

        支持单条/批量插入、REPLACE INTO、INSERT IGNORE 以及 ON DUPLICATE KEY UPDATE。
        PostgreSQL 和 SQLite 使用各自的 ON CONFLICT 语法。

        :param table: 表名
        :param data: 表数据，字典或字典列表
        :param auto_update: 是否使用 REPLACE INTO（完全覆盖已有数据）
        :param update_columns: ON DUPLICATE KEY UPDATE 时需要更新的列（指定后 auto_update 失效）
        :param update_columns_value: 更新列的对应值，字符串需手动加引号
        :param insert_ignore: 是否使用 INSERT IGNORE
        :param separator: 多条 SQL 的分隔符
        :param dialect: SQL 方言，支持 ``"mysql"``（默认）、``"postgresql"``、``"sqlite"``
        :param on_conflict: 冲突目标列元组，PostgreSQL 的 ``auto_update`` / ``update_columns``
            必须指定此参数
        :return: 插入 SQL 字符串

        ::

            >>> SqlUtil.make_insert_sql('user', {'name': 'Alice', 'age': 20})
            "INSERT INTO `user` (`name`,`age`) VALUES ('Alice', 20);\\n"
            >>> SqlUtil.make_insert_sql('user', {'name': 'Alice'}, insert_ignore=True, dialect='postgresql')
            'INSERT INTO "user" ("name") VALUES (\'Alice\') ON CONFLICT DO NOTHING;\\n'
        """
        SqlUtil._validate_dialect(dialect)

        def q(name):
            return SqlUtil._quote(name, dialect)

        if not data:
            return ""

        if isinstance(data, dict):
            fields = data.keys()
            values = SqlUtil._list2str([SqlUtil._format_sql_value(data[f]) for f in fields])
        elif isinstance(data, list):
            fields = data[0].keys()
            values = ", ".join([SqlUtil._list2str([SqlUtil._format_sql_value(d[f]) for f in fields]) for d in data])
        else:
            raise TypeError("生成插入 SQL 语句失败，数据必须是字典或者列表")

        values = values.replace("\x00", "")
        keys = [q(key) for key in fields]
        keys = SqlUtil._list2str(keys).replace("'", "")

        # ── MySQL 方言 ──────────────────────────────────────────
        if dialect == "mysql":
            ignore_ = " ignore" if insert_ignore else ""
            if update_columns:
                if not isinstance(update_columns, (tuple, list)):
                    update_columns = [update_columns]
                if update_columns_value:
                    update_columns_ = ", ".join([f"`{k}`={v}" for k, v in zip(update_columns, update_columns_value)])
                else:
                    update_columns_ = ", ".join([f"`{key}`=VALUES(`{key}`)" for key in update_columns])
                sql = f"INSERT{ignore_} INTO `{table}` {keys} VALUES {values} ON DUPLICATE KEY UPDATE {update_columns_}"
            elif auto_update:
                sql = f"REPLACE INTO `{table}` {keys} VALUES {values}"
            else:
                sql = f"INSERT{ignore_} INTO `{table}` {keys} VALUES {values}"
            sql = sql.replace("None", "null") + separator
            return sql

        # ── PostgreSQL / SQLite 方言 ────────────────────────────
        if update_columns:
            if not isinstance(update_columns, (tuple, list)):
                update_columns = [update_columns]
            conflict_cols = SqlUtil._conflict_cols(on_conflict, update_columns)
            conflict_target = ", ".join(conflict_cols)
            excluded = "EXCLUDED" if dialect == "postgresql" else "excluded"
            if update_columns_value:
                set_clause = ", ".join([f"{q(k)}={v}" for k, v in zip(update_columns, update_columns_value)])
            else:
                set_clause = ", ".join([f"{q(key)}={excluded}.{q(key)}" for key in update_columns])
            sql = f"INSERT INTO {q(table)} {keys} VALUES {values} ON CONFLICT ({conflict_target}) DO UPDATE SET {set_clause}"
        elif auto_update:
            if dialect == "sqlite":
                sql = f"INSERT OR REPLACE INTO {q(table)} {keys} VALUES {values}"
            else:
                # PostgreSQL 需要 on_conflict 来指定冲突列
                if not on_conflict:
                    raise ValueError("PostgreSQL 的 auto_update 模式必须指定 on_conflict 参数")
                conflict_cols = list(on_conflict)
                conflict_target = ", ".join(conflict_cols)
                all_cols = list(fields)
                set_clause = ", ".join([f"{q(c)}=EXCLUDED.{q(c)}" for c in all_cols])
                sql = (
                    f"INSERT INTO {q(table)} {keys} VALUES {values}"
                    f" ON CONFLICT ({conflict_target}) DO UPDATE SET {set_clause}"
                )
        elif insert_ignore:
            if dialect == "sqlite":
                sql = f"INSERT OR IGNORE INTO {q(table)} {keys} VALUES {values}"
            else:
                # PostgreSQL: ON CONFLICT DO NOTHING（无需指定冲突列）
                sql = f"INSERT INTO {q(table)} {keys} VALUES {values} ON CONFLICT DO NOTHING"
        else:
            sql = f"INSERT INTO {q(table)} {keys} VALUES {values}"

        sql = sql.replace("None", "null") + separator
        return sql

    @staticmethod
    def make_update_sql(
        table: str,
        data: dict,
        condition: str,
        separator: str = ";\n",
        dialect: str = "mysql",
    ) -> str:
        """生成更新 SQL。

        :param table: 表名
        :param data: 要更新的字段和值
        :param condition: WHERE 条件（不含 WHERE 关键字）
        :param separator: SQL 结尾分隔符
        :param dialect: SQL 方言，支持 ``"mysql"``（默认）、``"postgresql"``、``"sqlite"``
        :return: 更新 SQL 字符串

        ::

            >>> SqlUtil.make_update_sql('user', {'name': 'Bob'}, 'id = 1')
            "UPDATE `user` SET `name`='Bob' WHERE id = 1;\\n"
            >>> SqlUtil.make_update_sql('user', {'name': 'Bob'}, 'id = 1', dialect='postgresql')
            "UPDATE \\"user\\" SET \\"name\\"='Bob' WHERE id = 1;\\n"
        """
        SqlUtil._validate_dialect(dialect)

        def q(name):
            return SqlUtil._quote(name, dialect)

        key_values = []

        for key, value in data.items():
            value = SqlUtil._format_sql_value(value)
            if isinstance(value, str):
                key_values.append(f"{q(key)}={value!r}")
            elif value is None:
                key_values.append("{}={}".format(q(key), "null"))
            else:
                key_values.append(f"{q(key)}={value}")

        key_values = ", ".join(key_values)

        sql = f"UPDATE {q(table)} SET {key_values} WHERE {condition}{separator}"
        return sql

    @staticmethod
    def make_delete_sql(table: str, condition: str, dialect: str = "mysql") -> str:
        """生成删除 SQL。

        :param table: 表名
        :param condition: WHERE 条件（不含 WHERE 关键字）
        :param dialect: SQL 方言，支持 ``"mysql"``（默认）、``"postgresql"``、``"sqlite"``
        :return: 删除 SQL 字符串

        ::

            >>> SqlUtil.make_delete_sql('user', 'id = 1')
            'DELETE FROM user WHERE id = 1'
        """
        SqlUtil._validate_dialect(dialect)
        sql = f"DELETE FROM {table} WHERE {condition}"
        return sql

    @staticmethod
    def create_bak_table_sql(
        table: Union[str, List[str]],
        bak_table: Optional[Union[str, List[str]]] = None,
        bak_date: Optional[str] = None,
        separator: str = ";\n",
        dialect: str = "mysql",
    ) -> str:
        """生成备份表 SQL（CREATE TABLE ... AS SELECT）。

        :param table: 原表名（支持字符串或列表）
        :param bak_table: 备份表名，为空时自动使用 ``{table}_{bak_date}`` 格式
        :param bak_date: 备份日期（格式 ``%Y%m%d``），默认为当天
        :param separator: 多条 SQL 的分隔符
        :param dialect: SQL 方言，支持 ``"mysql"``（默认）、``"postgresql"``、``"sqlite"``
        :return: 创建备份表 SQL 字符串
        :raises ValueError: 当 table 和 bak_table 长度不一致时

        ::

            >>> SqlUtil.create_bak_table_sql('user', bak_date='20240101')
            'create table user_20240101 as select * from user;\\n'
        """
        SqlUtil._validate_dialect(dialect)
        if isinstance(table, str):
            table = [table]
        if isinstance(bak_table, str):
            bak_table = [bak_table]

        if not bak_table:
            if not bak_date:
                bak_date = datetime.datetime.now().strftime("%Y%m%d")
            bak_table = [f"{t}_{bak_date}" for t in table]
        elif len(table) != len(bak_table):
            raise ValueError("指定了 bak_table 参数，但是 table 的长度和 bak_table 的长度不同。")

        sql_statements = [f"create table {bt} as select * from {t}{separator}" for t, bt in zip(table, bak_table)]
        return "".join(sql_statements)

    # ── 内部辅助方法 ──────────────────────────────────────────────

    @staticmethod
    def _validate_dialect(dialect: str) -> None:
        """校验方言参数是否合法。

        :param dialect: 方言名称
        :raises ValueError: 不支持的方言

        ::

            >>> SqlUtil._validate_dialect('mysql')  # 正常
            >>> SqlUtil._validate_dialect('oracle')  # doctest: +SKIP
            Traceback (most recent call last):
            ...
            ValueError: ...
        """
        if dialect not in _VALID_DIALECTS:
            raise ValueError(f"不支持的方言: {dialect!r}，支持: {_VALID_DIALECTS}")

    @staticmethod
    def _quote(name: str, dialect: str = "mysql") -> str:
        """根据方言引用标识符。

        MySQL/SQLite 使用反引号，PostgreSQL 使用双引号。

        :param name: 标识符名称
        :param dialect: 方言
        :return: 引用后的标识符

        ::

            >>> SqlUtil._quote('user', 'mysql')
            '`user`'
            >>> SqlUtil._quote('user', 'postgresql')
            '"user"'
        """
        if dialect == "postgresql":
            return f'"{name}"'
        return f"`{name}`"

    @staticmethod
    def _conflict_cols(on_conflict: Optional[tuple], update_columns: tuple) -> list:
        """确定冲突目标列。

        未指定 ``on_conflict`` 时使用 ``update_columns`` 作为冲突列。

        :param on_conflict: 显式指定的冲突列
        :param update_columns: 需要更新的列
        :return: 冲突列列表
        """
        if on_conflict:
            return list(on_conflict)
        return list(update_columns)

    @staticmethod
    def _list2str(data: list) -> str:
        """将列表转为 SQL 元组字符串。

        :param data: 数据列表
        :return: 元组格式字符串，如 ``(1, 2)``

        ::

            >>> SqlUtil._list2str([1, 2])
            '(1, 2)'
            >>> SqlUtil._list2str([1])
            '(1)'
        """
        data_str = str(tuple(data))
        data_str = re.sub(r",\)$", ")", data_str)
        return data_str

    @staticmethod
    def _format_sql_value(value: Any) -> Any:
        """格式化 SQL 值。

        处理以下类型：
        - ``str``：包含子查询时用 ``${}`` 包裹
        - ``list`` / ``dict``：转为 JSON 字符串
        - ``datetime.date`` / ``datetime.time`` / ``datetime.datetime``：格式化为字符串
        - ``bool``：转为 ``0`` / ``1``
        - numpy 浮点/整数类型（可选，需安装 numpy）

        :param value: 原始值
        :return: 格式化后的值

        ::

            >>> SqlUtil._format_sql_value(True)
            1
            >>> SqlUtil._format_sql_value({'key': 'value'})
            '{"key": "value"}'
        """
        if isinstance(value, str):
            value = value.strip()
            if "select" in value.lower():
                value = "\x00" + value + "\x00"
        elif isinstance(value, (list, dict)):
            value = json.dumps(value)
        elif isinstance(value, datetime.datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, datetime.date):
            value = value.strftime("%Y-%m-%d")
        elif isinstance(value, datetime.time):
            value = value.strftime("%H:%M:%S")
        elif isinstance(value, bool):
            value = int(value)
        elif isinstance(value, _NUMPY_FLOAT_TYPES):
            value = float(value)
        elif isinstance(value, _NUMPY_INT_TYPES):
            value = int(value)
        return value

    # ── 链式调用工厂方法 ─────────────────────────────────────────

    @staticmethod
    def select(table: str, dialect: str = "mysql") -> "SelectBuilder":
        """创建 SELECT 链式构建器。

        :param table: 表名
        :param dialect: SQL 方言
        :return: SelectBuilder 实例

        ::

            >>> sql = SqlUtil.select('user').columns('name', 'age').where(age__gt=18).sql()
        """
        return SelectBuilder(table, dialect)

    @staticmethod
    def insert(table: str, dialect: str = "mysql") -> "InsertBuilder":
        """创建 INSERT 链式构建器。

        :param table: 表名
        :param dialect: SQL 方言
        :return: InsertBuilder 实例
        """
        return InsertBuilder(table, dialect)

    @staticmethod
    def update(table: str, dialect: str = "mysql") -> "UpdateBuilder":
        """创建 UPDATE 链式构建器。

        :param table: 表名
        :param dialect: SQL 方言
        :return: UpdateBuilder 实例
        """
        return UpdateBuilder(table, dialect)

    @staticmethod
    def delete(table: str, dialect: str = "mysql") -> "DeleteBuilder":
        """创建 DELETE 链式构建器。

        :param table: 表名
        :param dialect: SQL 方言
        :return: DeleteBuilder 实例
        """
        return DeleteBuilder(table, dialect)

    @staticmethod
    def create_table(table: str, dialect: str = "mysql") -> "CreateTableBuilder":
        """创建 CREATE TABLE 链式构建器。

        :param table: 表名
        :param dialect: SQL 方言
        :return: CreateTableBuilder 实例
        """
        return CreateTableBuilder(table, dialect)


# ═══════════════════════════════════════════════════════════════════
# Q — 条件组合器
# ═══════════════════════════════════════════════════════════════════


class Q:
    """条件组合器，支持 ``AND(&)``、``OR(|)``、``NOT(~)``。

    :param _connector: 内部连接符 ``"AND"`` 或 ``"OR"``
    :param _negated: 是否取反
    :param _q_children: 子 Q 对象列表（由 ``|`` / ``&`` 运算产生）
    :param kwargs: 过滤条件，支持 ``field__op=value`` 语法

    ::

        >>> (Q(age__gt=18) | Q(role='admin')).to_sql(SqlUtil._quote, SqlUtil._format_sql_value, 'mysql')
        '(`age`>18 OR `role`='admin')'
    """

    # 过算符映射
    _OPS = {
        "gt": ">",
        "gte": ">=",
        "lt": "<",
        "lte": "<=",
        "ne": "!=",
        "in": "IN",
        "not_in": "NOT IN",
        "between": "BETWEEN",
        "like": "LIKE",
        "contains": "CONTAINS",
        "startswith": "STARTSWITH",
        "endswith": "ENDSWITH",
        "isnull": "ISNULL",
    }

    def __init__(
        self,
        _connector: str = "AND",
        _negated: bool = False,
        _q_children: Optional[List["Q"]] = None,
        **kwargs,
    ):
        self._connector = _connector
        self._negated = _negated
        self._filters = kwargs
        self._children: List[Q] = list(_q_children) if _q_children else []

    def __or__(self, other: "Q") -> "Q":
        return Q(_connector="OR", _q_children=[self, other])

    def __and__(self, other: "Q") -> "Q":
        return Q(_connector="AND", _q_children=[self, other])

    def __invert__(self) -> "Q":
        clone = Q(
            _connector=self._connector,
            _negated=not self._negated,
            _q_children=list(self._children),
            **self._filters,
        )
        return clone

    def to_sql(self, quote_fn, format_fn, dialect: str) -> str:
        """递归生成 SQL 条件字符串。

        :param quote_fn: 标识符引用函数
        :param format_fn: 值格式化函数
        :param dialect: SQL 方言
        :return: SQL 条件片段
        """
        parts = []

        # 处理自身过滤条件
        for key, value in self._filters.items():
            parts.append(Q._resolve_single_filter(key, value, quote_fn, format_fn, dialect))

        # 递归处理子 Q 对象
        for child in self._children:
            child_sql = child.to_sql(quote_fn, format_fn, dialect)
            parts.append(child_sql)

        if not parts:
            return ""

        if len(parts) == 1:
            result = parts[0]
        else:
            joined = f" {self._connector} ".join(parts)
            result = f"({joined})"

        if self._negated:
            result = f"NOT {result}"

        return result

    @staticmethod
    def _resolve_single_filter(key: str, value, quote_fn, format_fn, dialect: str) -> str:
        """解析单个 field__op=value 条件。"""

        def _resolve_val(v):
            """解析值：F 对象转 SQL，其他格式化。"""
            if isinstance(v, F):
                return v.to_sql(quote_fn, dialect)
            fmt = format_fn(v)
            if isinstance(fmt, str):
                return repr(fmt)
            return str(fmt)

        # 拆分 field 和 operator
        parts = key.split("__")
        if len(parts) >= 2 and parts[-1] in Q._OPS:
            field = "__".join(parts[:-1])
            op = parts[-1]
        else:
            field = key
            op = None

        q_field = quote_fn(field, dialect) if not field.startswith("(") else field

        if op is None:
            if value is None:
                return f"{q_field} IS NULL"
            return f"{q_field}={_resolve_val(value)}"

        sql_op = Q._OPS[op]

        if op == "isnull":
            if value:
                return f"{q_field} IS NULL"
            return f"{q_field} IS NOT NULL"

        if op == "in":
            if not value:
                return "1=0"
            formatted = ", ".join([_resolve_val(v) for v in value])
            return f"{q_field} IN ({formatted})"

        if op == "not_in":
            if not value:
                return "1=1"
            formatted = ", ".join([_resolve_val(v) for v in value])
            return f"{q_field} NOT IN ({formatted})"

        if op == "between":
            lo, hi = value
            return f"{q_field} BETWEEN {_resolve_val(lo)} AND {_resolve_val(hi)}"

        if op == "contains":
            return f"{q_field} LIKE '%{value}%'"

        if op == "startswith":
            return f"{q_field} LIKE '{value}%'"

        if op == "endswith":
            return f"{q_field} LIKE '%{value}'"

        # gt, gte, lt, lte, ne, like
        return f"{q_field}{sql_op}{_resolve_val(value)}"


# ═══════════════════════════════════════════════════════════════════
# F — 字段引用
# ═══════════════════════════════════════════════════════════════════


class F:
    """字段引用，支持算术运算和聚合函数。

    :param name: 字段名

    ::

        >>> (F('balance') + 100).to_sql(SqlUtil._quote, 'mysql')
        '`balance`+100'
        >>> F.count('*').to_sql(SqlUtil._quote, 'mysql')
        'COUNT(*)'
    """

    def __init__(self, name: str):
        self._name = name
        self._ops: List[Tuple[str, Any]] = []
        self._is_agg = False
        self._agg_func: Optional[str] = None

    def __add__(self, other):
        return self._clone("+", other)

    def __radd__(self, other):
        clone = F(self._name)
        clone._ops = [(other, "+"), *list(self._ops)]
        clone._is_agg = self._is_agg
        clone._agg_func = self._agg_func
        return clone

    def __sub__(self, other):
        return self._clone("-", other)

    def __rsub__(self, other):
        clone = F(self._name)
        clone._ops = [(other, "-"), *list(self._ops)]
        clone._is_agg = self._is_agg
        clone._agg_func = self._agg_func
        return clone

    def __mul__(self, other):
        return self._clone("*", other)

    def __rmul__(self, other):
        clone = F(self._name)
        clone._ops = [(other, "*"), *list(self._ops)]
        clone._is_agg = self._is_agg
        clone._agg_func = self._agg_func
        return clone

    def __truediv__(self, other):
        return self._clone("/", other)

    def __rtruediv__(self, other):
        clone = F(self._name)
        clone._ops = [(other, "/"), *list(self._ops)]
        clone._is_agg = self._is_agg
        clone._agg_func = self._agg_func
        return clone

    def __neg__(self):
        clone = F(self._name)
        clone._ops = [("_neg", None), *list(self._ops)]
        clone._is_agg = self._is_agg
        clone._agg_func = self._agg_func
        return clone

    def _clone(self, op: str, value):
        clone = F(self._name)
        clone._ops = [*list(self._ops), (op, value)]
        clone._is_agg = self._is_agg
        clone._agg_func = self._agg_func
        return clone

    @staticmethod
    def count(name: str = "*") -> "F":
        """COUNT 聚合。"""
        f = F(name)
        f._is_agg = True
        f._agg_func = "COUNT"
        return f

    @staticmethod
    def sum(name: str) -> "F":
        """SUM 聚合。"""
        f = F(name)
        f._is_agg = True
        f._agg_func = "SUM"
        return f

    @staticmethod
    def max(name: str) -> "F":
        """MAX 聚合。"""
        f = F(name)
        f._is_agg = True
        f._agg_func = "MAX"
        return f

    @staticmethod
    def min(name: str) -> "F":
        """MIN 聚合。"""
        f = F(name)
        f._is_agg = True
        f._agg_func = "MIN"
        return f

    @staticmethod
    def avg(name: str) -> "F":
        """AVG 聚合。"""
        f = F(name)
        f._is_agg = True
        f._agg_func = "AVG"
        return f

    def to_sql(self, quote_fn, dialect: str = "mysql") -> str:
        """生成字段引用 SQL 片段。

        :param quote_fn: 标识符引用函数
        :param dialect: SQL 方言
        :return: SQL 表达式
        """
        if self._is_agg:
            if self._name == "*":
                base = f"{self._agg_func}(*)"
            else:
                base = f"{self._agg_func}({quote_fn(self._name, dialect)})"
        elif self._name == "*":
            base = "*"
        elif self._name.startswith("("):
            base = self._name
        else:
            base = quote_fn(self._name, dialect)

        for op, val in self._ops:
            if op == "_neg":
                base = f"-{base}"
            else:
                rhs = quote_fn(val, dialect) if isinstance(val, str) and not val.startswith("(") else str(val)
                base = f"{base}{op}{rhs}"

        return base


# ═══════════════════════════════════════════════════════════════════
# ColumnType — 列类型枚举
# ═══════════════════════════════════════════════════════════════════


class ColumnType(enum.Enum):
    """列类型枚举，自动适配 MySQL / PostgreSQL / SQLite 方言。

    ::

        >>> ColumnType.VARCHAR.to_sql('mysql', '(100)')
        'VARCHAR(100)'
        >>> ColumnType.SERIAL.to_sql('postgresql')
        'SERIAL'
        >>> ColumnType.BOOLEAN.to_sql('mysql')
        'TINYINT(1)'
    """

    # 整数
    TINYINT = "TINYINT"
    SMALLINT = "SMALLINT"
    MEDIUMINT = "MEDIUMINT"
    INT = "INT"
    BIGINT = "BIGINT"
    # 自增
    SERIAL = "SERIAL"
    BIG_SERIAL = "BIG_SERIAL"
    # 浮点
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    REAL = "REAL"
    DECIMAL = "DECIMAL"
    NUMERIC = "NUMERIC"
    # 字符串
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"
    TINYTEXT = "TINYTEXT"
    TEXT = "TEXT"
    MEDIUMTEXT = "MEDIUMTEXT"
    LONGTEXT = "LONGTEXT"
    # 二进制
    TINYBLOB = "TINYBLOB"
    BLOB = "BLOB"
    MEDIUMBLOB = "MEDIUMBLOB"
    LONGBLOB = "LONGBLOB"
    BINARY = "BINARY"
    VARBINARY = "VARBINARY"
    BYTEA = "BYTEA"
    # 日期时间
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    # 布尔
    BOOLEAN = "BOOLEAN"
    # JSON
    JSON = "JSON"
    JSONB = "JSONB"
    # UUID
    UUID = "UUID"
    # 枚举
    ENUM = "ENUM"

    def to_sql(self, dialect: str, type_args: Optional[str] = None) -> str:
        """获取对应方言的 SQL 类型字符串。

        :param dialect: SQL 方言
        :param type_args: 类型参数，如 ``"(100)"``、``"(10,2)"``
        :return: SQL 类型字符串
        """
        base = _COLUMN_DIALECT_MAP.get(self, {}).get(dialect, self.value)
        if type_args:
            return f"{base}{type_args}"
        return base


# 方言映射表（模块级，避免 enum metaclass 干扰）
_COLUMN_DIALECT_MAP: Dict[ColumnType, Dict[str, str]] = {
    ColumnType.TINYINT: {"mysql": "TINYINT", "postgresql": "SMALLINT", "sqlite": "INTEGER"},
    ColumnType.SMALLINT: {"mysql": "SMALLINT", "postgresql": "SMALLINT", "sqlite": "INTEGER"},
    ColumnType.MEDIUMINT: {"mysql": "MEDIUMINT", "postgresql": "INTEGER", "sqlite": "INTEGER"},
    ColumnType.INT: {"mysql": "INT", "postgresql": "INTEGER", "sqlite": "INTEGER"},
    ColumnType.BIGINT: {"mysql": "BIGINT", "postgresql": "BIGINT", "sqlite": "INTEGER"},
    ColumnType.SERIAL: {"mysql": "INT AUTO_INCREMENT", "postgresql": "SERIAL", "sqlite": "INTEGER"},
    ColumnType.BIG_SERIAL: {"mysql": "BIGINT AUTO_INCREMENT", "postgresql": "BIGSERIAL", "sqlite": "INTEGER"},
    ColumnType.FLOAT: {"mysql": "FLOAT", "postgresql": "REAL", "sqlite": "REAL"},
    ColumnType.DOUBLE: {"mysql": "DOUBLE", "postgresql": "DOUBLE PRECISION", "sqlite": "REAL"},
    ColumnType.REAL: {"mysql": "REAL", "postgresql": "REAL", "sqlite": "REAL"},
    ColumnType.DECIMAL: {"mysql": "DECIMAL", "postgresql": "DECIMAL", "sqlite": "NUMERIC"},
    ColumnType.NUMERIC: {"mysql": "NUMERIC", "postgresql": "NUMERIC", "sqlite": "NUMERIC"},
    ColumnType.CHAR: {"mysql": "CHAR", "postgresql": "CHAR", "sqlite": "TEXT"},
    ColumnType.VARCHAR: {"mysql": "VARCHAR", "postgresql": "VARCHAR", "sqlite": "TEXT"},
    ColumnType.TINYTEXT: {"mysql": "TINYTEXT", "postgresql": "TEXT", "sqlite": "TEXT"},
    ColumnType.TEXT: {"mysql": "TEXT", "postgresql": "TEXT", "sqlite": "TEXT"},
    ColumnType.MEDIUMTEXT: {"mysql": "MEDIUMTEXT", "postgresql": "TEXT", "sqlite": "TEXT"},
    ColumnType.LONGTEXT: {"mysql": "LONGTEXT", "postgresql": "TEXT", "sqlite": "TEXT"},
    ColumnType.TINYBLOB: {"mysql": "TINYBLOB", "postgresql": "BYTEA", "sqlite": "BLOB"},
    ColumnType.BLOB: {"mysql": "BLOB", "postgresql": "BYTEA", "sqlite": "BLOB"},
    ColumnType.MEDIUMBLOB: {"mysql": "MEDIUMBLOB", "postgresql": "BYTEA", "sqlite": "BLOB"},
    ColumnType.LONGBLOB: {"mysql": "LONGBLOB", "postgresql": "BYTEA", "sqlite": "BLOB"},
    ColumnType.BINARY: {"mysql": "BINARY", "postgresql": "BYTEA", "sqlite": "BLOB"},
    ColumnType.VARBINARY: {"mysql": "VARBINARY", "postgresql": "BYTEA", "sqlite": "BLOB"},
    ColumnType.BYTEA: {"mysql": "BLOB", "postgresql": "BYTEA", "sqlite": "BLOB"},
    ColumnType.DATE: {"mysql": "DATE", "postgresql": "DATE", "sqlite": "TEXT"},
    ColumnType.TIME: {"mysql": "TIME", "postgresql": "TIME", "sqlite": "TEXT"},
    ColumnType.DATETIME: {"mysql": "DATETIME", "postgresql": "TIMESTAMP", "sqlite": "TEXT"},
    ColumnType.TIMESTAMP: {"mysql": "TIMESTAMP", "postgresql": "TIMESTAMP", "sqlite": "TEXT"},
    ColumnType.BOOLEAN: {"mysql": "TINYINT(1)", "postgresql": "BOOLEAN", "sqlite": "INTEGER"},
    ColumnType.JSON: {"mysql": "JSON", "postgresql": "JSONB", "sqlite": "TEXT"},
    ColumnType.JSONB: {"mysql": "JSON", "postgresql": "JSONB", "sqlite": "TEXT"},
    ColumnType.UUID: {"mysql": "CHAR(36)", "postgresql": "UUID", "sqlite": "TEXT"},
    ColumnType.ENUM: {"mysql": "ENUM", "postgresql": "VARCHAR(255)", "sqlite": "TEXT"},
}


# ═══════════════════════════════════════════════════════════════════
# SqlBuilder — 基类
# ═══════════════════════════════════════════════════════════════════


class SqlBuilder:
    """SQL 链式构建器基类。"""

    _FILTER_OPS = {
        "gt": ">",
        "gte": ">=",
        "lt": "<",
        "lte": "<=",
        "ne": "!=",
        "in": "IN",
        "not_in": "NOT IN",
        "between": "BETWEEN",
        "like": "LIKE",
        "contains": "CONTAINS",
        "startswith": "STARTSWITH",
        "endswith": "ENDSWITH",
        "isnull": "ISNULL",
    }

    def __init__(self, dialect: str = "mysql"):
        SqlUtil._validate_dialect(dialect)
        self._dialect = dialect

    def _q(self, name: str) -> str:
        """引用标识符。"""
        return SqlUtil._quote(name, self._dialect)

    def _clone(self):
        """浅拷贝当前状态。"""
        return copy.copy(self)

    def _format_value(self, val: Any) -> Any:
        """格式化值。"""
        return SqlUtil._format_sql_value(val)

    def _resolve_conditions(self, conditions: list) -> str:
        """将条件列表（Q 对象或原始字符串）转为 SQL WHERE 子句。"""
        parts = []
        for cond in conditions:
            if isinstance(cond, Q):
                parts.append(cond.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, self._dialect))
            elif isinstance(cond, str):
                parts.append(cond)
        return " AND ".join(parts) if parts else ""

    def _resolve_single_filter(self, key: str, value: Any) -> str:
        """解析单个 field__op=value 为 SQL 片段。"""
        return Q._resolve_single_filter(key, value, SqlUtil._quote, SqlUtil._format_sql_value, self._dialect)

    def _resolve_column(self, col) -> str:
        """解析列为 SQL 片段（F 对象或原始字符串或普通列名）。"""
        if isinstance(col, F):
            return col.to_sql(SqlUtil._quote, self._dialect)
        if isinstance(col, str) and (col == "*" or "(" in col or " " in col or "." in col):
            return col
        return self._q(str(col))

    def sql(self) -> str:
        """生成 SQL 字符串。"""
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════
# SelectBuilder
# ═══════════════════════════════════════════════════════════════════


class SelectBuilder(SqlBuilder):
    """SELECT 链式构建器。

    ::

        >>> (SqlUtil.select('user')
        ...     .columns('id', 'name', 'age')
        ...     .where(age__gt=18)
        ...     .order_by('-age', 'name')
        ...     .limit(10)
        ...     .sql())
        'SELECT `id`,`name`,`age` FROM `user` WHERE `age`>18 ORDER BY `age` DESC,`name` ASC LIMIT 10'
    """

    def __init__(self, table: str, dialect: str = "mysql"):
        super().__init__(dialect)
        self._table = table
        self._columns: List[str] = ["*"]
        self._conditions: list = []
        self._order_by: List[str] = []
        self._limit: Optional[int] = None
        self._offset_val: Optional[int] = None
        self._is_distinct = False
        self._group_by: List[str] = []
        self._having_conds: list = []

    def columns(self, *cols) -> "SelectBuilder":
        """指定查询列。可传原始 SQL 表达式。

        :param cols: 列名或 SQL 表达式
        :return: self（链式调用）
        """
        clone = self._clone()
        clone._columns = list(cols) if cols else ["*"]
        return clone

    def where(self, *args, **kwargs) -> "SelectBuilder":
        """添加 WHERE 条件。

        :param args: Q 对象或原始 SQL 字符串
        :param kwargs: ``field__op=value`` 格式的过滤条件
        :return: self（链式调用）
        """
        clone = self._clone()
        clone._conditions = list(self._conditions)
        if kwargs:
            clone._conditions.append(Q(**kwargs))
        for arg in args:
            clone._conditions.append(arg)
        return clone

    def where_raw(self, condition: str) -> "SelectBuilder":
        """添加原始 SQL WHERE 条件。"""
        clone = self._clone()
        clone._conditions = list(self._conditions)
        clone._conditions.append(condition)
        return clone

    def order_by(self, *fields) -> "SelectBuilder":
        """添加排序。前缀 ``-`` 表示 DESC。

        :param fields: 排序字段，如 ``"-age"``, ``"name"``
        :return: self（链式调用）
        """
        clone = self._clone()
        clone._order_by = list(self._order_by)
        for f in fields:
            if isinstance(f, str) and f.startswith("-"):
                clone._order_by.append(f"{self._resolve_column(f[1:])} DESC")
            elif isinstance(f, str) and (" " in f or "(" in f):
                # 原始 SQL 如 "FIELD(status, 'vip')"
                clone._order_by.append(f)
            else:
                clone._order_by.append(f"{self._resolve_column(f)} ASC")
        return clone

    def limit(self, n: int) -> "SelectBuilder":
        """设置 LIMIT。"""
        clone = self._clone()
        clone._limit = n
        return clone

    def offset(self, n: int) -> "SelectBuilder":
        """设置 OFFSET。"""
        clone = self._clone()
        clone._offset_val = n
        return clone

    def page(self, page_no: int, page_size: int) -> "SelectBuilder":
        """按页码设置分页。``page_no`` 从 1 开始。"""
        page_no = max(1, page_no)
        clone = self._clone()
        clone._limit = page_size
        clone._offset_val = (page_no - 1) * page_size
        return clone

    def distinct(self) -> "SelectBuilder":
        """SELECT DISTINCT。"""
        clone = self._clone()
        clone._is_distinct = True
        return clone

    def group_by(self, *fields) -> "SelectBuilder":
        """添加 GROUP BY。可传原始 SQL。"""
        clone = self._clone()
        clone._group_by = list(self._group_by)
        for f in fields:
            clone._group_by.append(self._resolve_column(f))
        return clone

    def having(self, *args, **kwargs) -> "SelectBuilder":
        """添加 HAVING 条件。参数同 ``where``。"""
        clone = self._clone()
        clone._having_conds = list(self._having_conds)
        if kwargs:
            clone._having_conds.append(Q(**kwargs))
        for arg in args:
            clone._having_conds.append(arg)
        return clone

    def sql(self) -> str:
        """生成 SELECT SQL。"""
        select_kw = "SELECT DISTINCT" if self._is_distinct else "SELECT"
        cols = ", ".join([self._resolve_column(c) for c in self._columns])
        sql = f"{select_kw} {cols} FROM {self._q(self._table)}"

        where = self._resolve_conditions(self._conditions)
        if where:
            sql += f" WHERE {where}"

        if self._group_by:
            sql += f" GROUP BY {','.join(self._group_by)}"

        if self._having_conds:
            having = self._resolve_conditions(self._having_conds)
            if having:
                sql += f" HAVING {having}"

        if self._order_by:
            sql += f" ORDER BY {','.join(self._order_by)}"

        if self._limit is not None:
            if self._dialect == "mysql":
                offset = self._offset_val or 0
                sql += f" LIMIT {offset}, {self._limit}"
            else:
                sql += f" LIMIT {self._limit}"
                if self._offset_val is not None:
                    sql += f" OFFSET {self._offset_val}"

        return sql


# ═══════════════════════════════════════════════════════════════════
# InsertBuilder
# ═══════════════════════════════════════════════════════════════════


class InsertBuilder(SqlBuilder):
    """INSERT 链式构建器。

    ::

        >>> (SqlUtil.insert('user', dialect='postgresql')
        ...     .values(name='Alice', age=20)
        ...     .on_conflict('id')
        ...     .do_update('name', 'age')
        ...     .sql())
        'INSERT INTO "user" ("name","age") VALUES (\'Alice\',20) ON CONFLICT (id) DO UPDATE SET "name"=EXCLUDED."name","age"=EXCLUDED."age"'
    """

    def __init__(self, table: str, dialect: str = "mysql"):
        super().__init__(dialect)
        self._table = table
        self._data: Optional[Union[dict, List[dict]]] = None
        self._on_conflict_cols: Optional[Tuple[str, ...]] = None
        self._do_update_cols: Optional[Tuple[str, ...]] = None
        self._do_update_values: Optional[Tuple[str, ...]] = None
        self._do_nothing = False
        self._ignore = False
        self._replace = False
        self._separator = ";\n"

    def values(self, **kwargs) -> "InsertBuilder":
        """设置插入数据（单条）。"""
        clone = self._clone()
        clone._data = kwargs
        return clone

    def values_list(self, data: List[dict]) -> "InsertBuilder":
        """设置批量插入数据。"""
        clone = self._clone()
        clone._data = data
        return clone

    def on_conflict(self, *cols) -> "InsertBuilder":
        """指定冲突目标列。"""
        clone = self._clone()
        clone._on_conflict_cols = cols
        return clone

    def do_update(self, *cols, values: Optional[Tuple[str, ...]] = None) -> "InsertBuilder":
        """ON CONFLICT DO UPDATE SET 指定列。

        :param cols: 需要更新的列
        :param values: 更新列的对应值（可选，手动加引号的字符串）
        """
        clone = self._clone()
        clone._do_update_cols = cols
        clone._do_update_values = values
        return clone

    def do_nothing(self) -> "InsertBuilder":
        """ON CONFLICT DO NOTHING。"""
        clone = self._clone()
        clone._do_nothing = True
        return clone

    def ignore(self) -> "InsertBuilder":
        """INSERT IGNORE / INSERT OR IGNORE。"""
        clone = self._clone()
        clone._ignore = True
        return clone

    def replace(self) -> "InsertBuilder":
        """REPLACE INTO / INSERT OR REPLACE。"""
        clone = self._clone()
        clone._replace = True
        return clone

    def separator(self, sep: str) -> "InsertBuilder":
        """设置 SQL 结尾分隔符。"""
        clone = self._clone()
        clone._separator = sep
        return clone

    def sql(self) -> str:
        """生成 INSERT SQL。"""
        if not self._data:
            return ""

        data = self._data
        if isinstance(data, dict):
            fields = list(data.keys())
            vals = SqlUtil._list2str([self._format_value(data[f]) for f in fields])
        elif isinstance(data, list):
            fields = list(data[0].keys())
            vals = ", ".join([SqlUtil._list2str([self._format_value(d[f]) for f in fields]) for d in data])
        else:
            raise TypeError("数据必须是字典或列表")

        vals = vals.replace("\x00", "")
        keys = [self._q(k) for k in fields]
        keys_str = SqlUtil._list2str(keys).replace("'", "")

        conflict_cols = self._on_conflict_cols
        do_update_cols = self._do_update_cols

        # ── MySQL ──
        if self._dialect == "mysql":
            ignore_ = " ignore" if self._ignore else ""
            if do_update_cols:
                conflict_target = conflict_cols or do_update_cols
                if self._do_update_values:
                    set_clause = ", ".join([f"`{k}`={v}" for k, v in zip(do_update_cols, self._do_update_values)])
                else:
                    set_clause = ", ".join([f"`{c}`=VALUES(`{c}`)" for c in do_update_cols])
                sql = f"INSERT{ignore_} INTO `{self._table}` {keys_str} VALUES {vals} ON DUPLICATE KEY UPDATE {set_clause}"
            elif self._replace:
                sql = f"REPLACE INTO `{self._table}` {keys_str} VALUES {vals}"
            else:
                sql = f"INSERT{ignore_} INTO `{self._table}` {keys_str} VALUES {vals}"
            sql = sql.replace("None", "null") + self._separator
            return sql

        # ── PostgreSQL / SQLite ──
        q_table = self._q(self._table)
        excluded = "EXCLUDED" if self._dialect == "postgresql" else "excluded"

        if do_update_cols:
            conflict_target = conflict_cols or do_update_cols
            ct = ", ".join(conflict_target)
            if self._do_update_values:
                set_clause = ", ".join([f"{self._q(k)}={v}" for k, v in zip(do_update_cols, self._do_update_values)])
            else:
                set_clause = ", ".join([f"{self._q(c)}={excluded}.{self._q(c)}" for c in do_update_cols])
            sql = f"INSERT INTO {q_table} {keys_str} VALUES {vals} ON CONFLICT ({ct}) DO UPDATE SET {set_clause}"
        elif self._do_nothing:
            if self._dialect == "sqlite":
                sql = f"INSERT OR IGNORE INTO {q_table} {keys_str} VALUES {vals}"
            else:
                sql = f"INSERT INTO {q_table} {keys_str} VALUES {vals} ON CONFLICT DO NOTHING"
        elif self._replace:
            if self._dialect == "sqlite":
                sql = f"INSERT OR REPLACE INTO {q_table} {keys_str} VALUES {vals}"
            else:
                if not conflict_cols:
                    raise ValueError("PostgreSQL 的 replace 模式必须指定 on_conflict 参数")
                ct = ", ".join(conflict_cols)
                all_cols = list(fields)
                set_clause = ", ".join([f"{self._q(c)}=EXCLUDED.{self._q(c)}" for c in all_cols])
                sql = f"INSERT INTO {q_table} {keys_str} VALUES {vals} ON CONFLICT ({ct}) DO UPDATE SET {set_clause}"
        elif self._ignore:
            if self._dialect == "sqlite":
                sql = f"INSERT OR IGNORE INTO {q_table} {keys_str} VALUES {vals}"
            else:
                sql = f"INSERT INTO {q_table} {keys_str} VALUES {vals} ON CONFLICT DO NOTHING"
        else:
            sql = f"INSERT INTO {q_table} {keys_str} VALUES {vals}"

        sql = sql.replace("None", "null") + self._separator
        return sql


# ═══════════════════════════════════════════════════════════════════
# UpdateBuilder
# ═══════════════════════════════════════════════════════════════════


class UpdateBuilder(SqlBuilder):
    """UPDATE 链式构建器。

    ::

        >>> (SqlUtil.update('user')
        ...     .set(name='Bob', age=30)
        ...     .where(id=1)
        ...     .sql())
        "UPDATE `user` SET `name`='Bob',`age`=30 WHERE `id`=1;\\n"
    """

    def __init__(self, table: str, dialect: str = "mysql"):
        super().__init__(dialect)
        self._table = table
        self._sets: List[str] = []
        self._conditions: list = []
        self._separator = ";\n"

    def set(self, **kwargs) -> "UpdateBuilder":
        """设置更新字段。值可以是 F 对象。

        :param kwargs: ``field=value`` 格式
        :return: self（链式调用）
        """
        clone = self._clone()
        clone._sets = list(self._sets)
        for key, value in kwargs.items():
            if isinstance(value, F):
                clone._sets.append(f"{self._q(key)}={value.to_sql(SqlUtil._quote, self._dialect)}")
            else:
                fmt = self._format_value(value)
                if fmt is None:
                    clone._sets.append(f"{self._q(key)}=null")
                elif isinstance(fmt, str):
                    clone._sets.append(f"{self._q(key)}={fmt!r}")
                else:
                    clone._sets.append(f"{self._q(key)}={fmt}")
        return clone

    def set_raw(self, *raw_sqls) -> "UpdateBuilder":
        """设置原始 SQL SET 子句。"""
        clone = self._clone()
        clone._sets = list(self._sets)
        for raw in raw_sqls:
            clone._sets.append(raw)
        return clone

    def where(self, *args, **kwargs) -> "UpdateBuilder":
        """添加 WHERE 条件。"""
        clone = self._clone()
        clone._conditions = list(self._conditions)
        if kwargs:
            clone._conditions.append(Q(**kwargs))
        for arg in args:
            clone._conditions.append(arg)
        return clone

    def where_raw(self, condition: str) -> "UpdateBuilder":
        """添加原始 SQL WHERE 条件。"""
        clone = self._clone()
        clone._conditions = list(self._conditions)
        clone._conditions.append(condition)
        return clone

    def separator(self, sep: str) -> "UpdateBuilder":
        """设置 SQL 结尾分隔符。"""
        clone = self._clone()
        clone._separator = sep
        return clone

    def sql(self) -> str:
        """生成 UPDATE SQL。"""
        set_clause = ", ".join(self._sets)
        sql = f"UPDATE {self._q(self._table)} SET {set_clause}"

        where = self._resolve_conditions(self._conditions)
        if where:
            sql += f" WHERE {where}"

        return sql + self._separator


# ═══════════════════════════════════════════════════════════════════
# DeleteBuilder
# ═══════════════════════════════════════════════════════════════════


class DeleteBuilder(SqlBuilder):
    """DELETE 链式构建器。

    ::

        >>> (SqlUtil.delete('user')
        ...     .where(status='inactive', created_at__lt='2020-01-01')
        ...     .sql())
        "DELETE FROM `user` WHERE `status`='inactive' AND `created_at`<'2020-01-01'"
    """

    def __init__(self, table: str, dialect: str = "mysql"):
        super().__init__(dialect)
        self._table = table
        self._conditions: list = []

    def where(self, *args, **kwargs) -> "DeleteBuilder":
        """添加 WHERE 条件。"""
        clone = self._clone()
        clone._conditions = list(self._conditions)
        if kwargs:
            clone._conditions.append(Q(**kwargs))
        for arg in args:
            clone._conditions.append(arg)
        return clone

    def where_raw(self, condition: str) -> "DeleteBuilder":
        """添加原始 SQL WHERE 条件。"""
        clone = self._clone()
        clone._conditions = list(self._conditions)
        clone._conditions.append(condition)
        return clone

    def sql(self) -> str:
        """生成 DELETE SQL。"""
        sql = f"DELETE FROM {self._q(self._table)}"
        where = self._resolve_conditions(self._conditions)
        if where:
            sql += f" WHERE {where}"
        return sql


# ═══════════════════════════════════════════════════════════════════
# CreateTableBuilder
# ═══════════════════════════════════════════════════════════════════


class CreateTableBuilder(SqlBuilder):
    """CREATE TABLE 链式构建器。

    使用 ``ColumnType`` 枚举自动适配不同方言的列类型。

    ::

        >>> from hutool.core.sql import ColumnType as CT
        >>> (SqlUtil.create_table('user')
        ...     .column('id', CT.SERIAL, primary_key=True)
        ...     .column('name', CT.VARCHAR, type_args='(100)', nullable=False)
        ...     .column('age', CT.INT, default=0)
        ...     .if_not_exists()
        ...     .sql())
        'CREATE TABLE IF NOT EXISTS `user` (`id` INT AUTO_INCREMENT PRIMARY KEY,`name` VARCHAR(100) NOT NULL,`age` INT DEFAULT 0)'
    """

    def __init__(self, table: str, dialect: str = "mysql"):
        super().__init__(dialect)
        self._table = table
        self._columns: List[dict] = []
        self._pk_cols: Optional[Tuple[str, ...]] = None
        self._if_not_exists = False
        self._engine: Optional[str] = None
        self._charset: Optional[str] = None
        self._separator = ";\n"

    def column(
        self,
        name: str,
        col_type: ColumnType,
        type_args: Optional[str] = None,
        primary_key: bool = False,
        nullable: bool = True,
        default: Any = None,
        auto_increment: bool = False,
        unique: bool = False,
        comment: Optional[str] = None,
    ) -> "CreateTableBuilder":
        """定义列。

        :param name: 列名
        :param col_type: ``ColumnType`` 枚举
        :param type_args: 类型参数，如 ``"(100)"``、``"(10,2)"``
        :param primary_key: 是否为主键
        :param nullable: 是否允许 NULL
        :param default: 默认值
        :param auto_increment: 是否自增（MySQL 方言）
        :param unique: 是否唯一
        :param comment: 列注释（MySQL）
        :return: self（链式调用）
        """
        clone = self._clone()
        clone._columns = list(self._columns)
        clone._columns.append(
            {
                "name": name,
                "col_type": col_type,
                "type_args": type_args,
                "primary_key": primary_key,
                "nullable": nullable,
                "default": default,
                "auto_increment": auto_increment,
                "unique": unique,
                "comment": comment,
            }
        )
        return clone

    def if_not_exists(self) -> "CreateTableBuilder":
        """添加 IF NOT EXISTS。"""
        clone = self._clone()
        clone._if_not_exists = True
        return clone

    def primary_key(self, *cols) -> "CreateTableBuilder":
        """设置复合主键。"""
        clone = self._clone()
        clone._pk_cols = cols
        return clone

    def engine(self, name: str) -> "CreateTableBuilder":
        """设置存储引擎（MySQL）。"""
        clone = self._clone()
        clone._engine = name
        return clone

    def charset(self, name: str) -> "CreateTableBuilder":
        """设置字符集（MySQL）。"""
        clone = self._clone()
        clone._charset = name
        return clone

    def separator(self, sep: str) -> "CreateTableBuilder":
        """设置 SQL 结尾分隔符。"""
        clone = self._clone()
        clone._separator = sep
        return clone

    def sql(self) -> str:
        """生成 CREATE TABLE DDL。"""
        ine = " IF NOT EXISTS" if self._if_not_exists else ""
        col_defs = []

        for c in self._columns:
            dtype = c["col_type"].to_sql(self._dialect, c.get("type_args"))
            parts = [self._q(c["name"]), dtype]

            if c["primary_key"]:
                parts.append("PRIMARY KEY")
            if c["auto_increment"] and self._dialect == "mysql":
                parts.append("AUTO_INCREMENT")
            if not c["nullable"]:
                parts.append("NOT NULL")
            if c["unique"]:
                parts.append("UNIQUE")
            if c["default"] is not None:
                default = c["default"]
                if isinstance(default, bool):
                    default = "true" if default else "false"
                elif isinstance(default, str):
                    default = f"'{default}'"
                parts.append(f"DEFAULT {default}")
            if c["comment"] and self._dialect == "mysql":
                parts.append(f"COMMENT '{c['comment']}'")

            col_defs.append(" ".join(parts))

        # 复合主键
        if self._pk_cols:
            pk = ", ".join([self._q(c) for c in self._pk_cols])
            col_defs.append(f"PRIMARY KEY ({pk})")

        cols_str = ",".join(col_defs)
        sql = f"CREATE TABLE{ine} {self._q(self._table)} ({cols_str})"

        # MySQL 特有选项
        extras = []
        if self._engine:
            extras.append(f"ENGINE={self._engine}")
        if self._charset:
            extras.append(f"DEFAULT CHARSET={self._charset}")
        if extras:
            sql += " " + " ".join(extras)

        return sql + self._separator
