"""SQL 工具类。

提供 SQL 语句的生成工具，支持 SELECT、INSERT、UPDATE、DELETE 以及备份表创建。
值格式化支持 Python 内置类型和可选的 numpy 类型（无需安装 numpy）。
"""

import datetime
import json
import re
from typing import Any, List, Optional, Union

# numpy 可选支持：安装了 numpy 时自动识别其数值类型，未安装时零开销
try:
    import numpy as _np

    _NUMPY_FLOAT_TYPES = (_np.float16, _np.float32, _np.float64)
    _NUMPY_INT_TYPES = (_np.int8, _np.int16, _np.int32, _np.int64)
except ImportError:
    _NUMPY_FLOAT_TYPES = ()
    _NUMPY_INT_TYPES = ()


class SqlUtil:
    """SQL 工具类，用于生成常用 SQL 语句。

    支持 MySQL 风格的 INSERT ON DUPLICATE KEY UPDATE、REPLACE INTO、INSERT IGNORE
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
    ) -> str:
        """生成查询 SQL。

        :param table: 表名
        :param columns: 要查询的字段名，列表或原始字符串
        :param condition: WHERE 条件（不含 WHERE 关键字）
        :param order_by: 排序字段列表
        :param page_no: 页码（从 1 开始）
        :param page_size: 每页记录数
        :return: 查询 SQL 字符串

        ::

            >>> SqlUtil.make_select_sql('user', ['name', 'age'], 'id > 0')
            'SELECT `name`,`age` FROM `user` WHERE id > 0'
            >>> SqlUtil.make_select_sql('user', '*', page_no=2, page_size=10)
            'SELECT * FROM `user` LIMIT 10, 10'
        """
        if isinstance(columns, list):
            select_columns = ",".join([f"`{key}`" for key in columns])
        else:
            select_columns = columns
        sql = f"SELECT {select_columns} FROM `{table}`"
        if condition:
            sql += f" WHERE {condition}"
        if order_by:
            order_by_columns = ",".join([f"`{key}`" for key in order_by])
            sql += f" ORDER BY {order_by_columns}"
        if page_no is not None and page_size is not None:
            page_no = 1 if page_no < 1 else page_no
            limit = (page_no - 1) * page_size
            offset = page_size
            sql += f" LIMIT {limit}, {offset}"
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
    ) -> str:
        """生成插入 SQL。

        支持单条/批量插入、REPLACE INTO、INSERT IGNORE 以及 ON DUPLICATE KEY UPDATE。

        :param table: 表名
        :param data: 表数据，字典或字典列表
        :param auto_update: 是否使用 REPLACE INTO（完全覆盖已有数据）
        :param update_columns: ON DUPLICATE KEY UPDATE 时需要更新的列（指定后 auto_update 失效）
        :param update_columns_value: 更新列的对应值，字符串需手动加引号
        :param insert_ignore: 是否使用 INSERT IGNORE
        :param separator: 多条 SQL 的分隔符
        :return: 插入 SQL 字符串

        ::

            >>> SqlUtil.make_insert_sql('user', {'name': 'Alice', 'age': 20})
            "INSERT INTO `user` (`name`,`age`) VALUES ('Alice', 20);\\n"
        """
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
        keys = [f"`{key}`" for key in fields]
        keys = SqlUtil._list2str(keys).replace("'", "")
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

    @staticmethod
    def make_update_sql(table: str, data: dict, condition: str, separator: str = ";\n") -> str:
        """生成更新 SQL。

        :param table: 表名
        :param data: 要更新的字段和值
        :param condition: WHERE 条件（不含 WHERE 关键字）
        :param separator: SQL 结尾分隔符
        :return: 更新 SQL 字符串

        ::

            >>> SqlUtil.make_update_sql('user', {'name': 'Bob'}, 'id = 1')
            "UPDATE `user` SET `name`='Bob' WHERE id = 1;\\n"
        """
        key_values = []

        for key, value in data.items():
            value = SqlUtil._format_sql_value(value)
            if isinstance(value, str):
                key_values.append(f"`{key}`={value!r}")
            elif value is None:
                key_values.append("`{}`={}".format(key, "null"))
            else:
                key_values.append(f"`{key}`={value}")

        key_values = ", ".join(key_values)

        sql = f"UPDATE `{table}` SET {key_values} WHERE {condition}{separator}"
        return sql

    @staticmethod
    def make_delete_sql(table: str, condition: str) -> str:
        """生成删除 SQL。

        :param table: 表名
        :param condition: WHERE 条件（不含 WHERE 关键字）
        :return: 删除 SQL 字符串

        ::

            >>> SqlUtil.make_delete_sql('user', 'id = 1')
            'DELETE FROM user WHERE id = 1'
        """
        sql = f"DELETE FROM {table} WHERE {condition}"
        return sql

    @staticmethod
    def create_bak_table_sql(
        table: Union[str, List[str]],
        bak_table: Optional[Union[str, List[str]]] = None,
        bak_date: Optional[str] = None,
        separator: str = ";\n",
    ) -> str:
        """生成备份表 SQL（CREATE TABLE ... AS SELECT）。

        :param table: 原表名（支持字符串或列表）
        :param bak_table: 备份表名，为空时自动使用 ``{table}_{bak_date}`` 格式
        :param bak_date: 备份日期（格式 ``%Y%m%d``），默认为当天
        :param separator: 多条 SQL 的分隔符
        :return: 创建备份表 SQL 字符串
        :raises ValueError: 当 table 和 bak_table 长度不一致时

        ::

            >>> SqlUtil.create_bak_table_sql('user', bak_date='20240101')
            'create table user_20240101 as select * from user;\\n'
        """
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

    # ── 内部方法 ──────────────────────────────────────────────────

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
