"""SqlUtil 测试"""

import datetime

import pytest

from hutool import SqlUtil


class TestMakeSelectSql:
    def test_basic(self):
        sql = SqlUtil.make_select_sql("user", ["name", "age"])
        assert sql == "SELECT `name`,`age` FROM `user`"

    def test_string_columns(self):
        sql = SqlUtil.make_select_sql("user", "*")
        assert sql == "SELECT * FROM `user`"

    def test_with_condition(self):
        sql = SqlUtil.make_select_sql("user", ["name"], "id > 0")
        assert "WHERE id > 0" in sql

    def test_with_order_by(self):
        sql = SqlUtil.make_select_sql("user", "*", order_by=["name", "age"])
        assert "ORDER BY `name`,`age`" in sql

    def test_with_pagination(self):
        sql = SqlUtil.make_select_sql("user", "*", page_no=2, page_size=10)
        assert "LIMIT 10, 10" in sql

    def test_page_no_less_than_1(self):
        sql = SqlUtil.make_select_sql("user", "*", page_no=0, page_size=10)
        assert "LIMIT 0, 10" in sql

    def test_full(self):
        sql = SqlUtil.make_select_sql(
            "user", ["id", "name"], condition="age > 18", order_by=["id"], page_no=1, page_size=5
        )
        assert "SELECT" in sql
        assert "WHERE" in sql
        assert "ORDER BY" in sql
        assert "LIMIT 0, 5" in sql


class TestMakeInsertSql:
    def test_single_dict(self):
        sql = SqlUtil.make_insert_sql("user", {"name": "Alice", "age": 20})
        assert "INSERT INTO" in sql
        assert "`user`" in sql
        assert "Alice" in sql
        assert sql.strip().endswith(";\n".strip())

    def test_batch_list(self):
        data = [{"name": "Alice", "age": 20}, {"name": "Bob", "age": 30}]
        sql = SqlUtil.make_insert_sql("user", data)
        assert "Alice" in sql
        assert "Bob" in sql

    def test_empty_data(self):
        assert SqlUtil.make_insert_sql("user", {}) == ""
        assert SqlUtil.make_insert_sql("user", []) == ""

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            SqlUtil.make_insert_sql("user", "invalid")

    def test_replace_into(self):
        sql = SqlUtil.make_insert_sql("user", {"name": "Alice"}, auto_update=True)
        assert "REPLACE INTO" in sql

    def test_insert_ignore(self):
        sql = SqlUtil.make_insert_sql("user", {"name": "Alice"}, insert_ignore=True)
        assert "INSERT ignore INTO" in sql

    def test_on_duplicate_key_update(self):
        sql = SqlUtil.make_insert_sql("user", {"name": "Alice", "age": 20}, update_columns=("name",))
        assert "ON DUPLICATE KEY UPDATE" in sql
        assert "`name`=VALUES(`name`)" in sql

    def test_on_duplicate_key_update_with_values(self):
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice"},
            update_columns=("name",),
            update_columns_value=("'Bob'",),
        )
        assert "`name`='Bob'" in sql

    def test_none_values_become_null(self):
        sql = SqlUtil.make_insert_sql("user", {"name": None})
        assert "null" in sql

    def test_list_value_becomes_json(self):
        sql = SqlUtil.make_insert_sql("user", {"tags": [1, 2, 3]})
        assert "[1, 2, 3]" in sql

    def test_dict_value_becomes_json(self):
        sql = SqlUtil.make_insert_sql("user", {"info": {"key": "val"}})
        assert '{"key": "val"}' in sql

    def test_datetime_value(self):
        dt = datetime.datetime(2024, 1, 15, 8, 30, 0)
        sql = SqlUtil.make_insert_sql("user", {"created": dt})
        assert "2024-01-15 08:30:00" in sql

    def test_date_value(self):
        d = datetime.date(2024, 1, 15)
        sql = SqlUtil.make_insert_sql("user", {"birthday": d})
        assert "2024-01-15" in sql

    def test_time_value(self):
        t = datetime.time(8, 30, 0)
        sql = SqlUtil.make_insert_sql("user", {"alarm": t})
        assert "08:30:00" in sql

    def test_bool_value(self):
        sql = SqlUtil.make_insert_sql("user", {"active": True})
        assert "1" in sql

    def test_subselect_value(self):
        sql = SqlUtil.make_insert_sql("user", {"name": "select 1"})
        # 子查询用 \x00 标记包裹后被去掉，保留引号
        assert "select 1" in sql

    def test_custom_separator(self):
        sql = SqlUtil.make_insert_sql("user", {"name": "A"}, separator=";")
        assert sql.endswith(";")


class TestMakeUpdateSql:
    def test_basic(self):
        sql = SqlUtil.make_update_sql("user", {"name": "Bob"}, "id = 1")
        assert "UPDATE `user` SET" in sql
        assert "WHERE id = 1" in sql

    def test_multiple_fields(self):
        sql = SqlUtil.make_update_sql("user", {"name": "Bob", "age": 30}, "id = 1")
        assert "`name`=" in sql
        assert "`age`=" in sql

    def test_none_value(self):
        sql = SqlUtil.make_update_sql("user", {"name": None}, "id = 1")
        assert "null" in sql


class TestMakeDeleteSql:
    def test_basic(self):
        sql = SqlUtil.make_delete_sql("user", "id = 1")
        assert sql == "DELETE FROM user WHERE id = 1"


class TestCreateBakTableSql:
    def test_basic(self):
        sql = SqlUtil.create_bak_table_sql("user", bak_date="20240101")
        assert "create table user_20240101 as select * from user" in sql

    def test_custom_bak_table(self):
        sql = SqlUtil.create_bak_table_sql("user", bak_table="user_backup")
        assert "create table user_backup as select * from user" in sql

    def test_multiple_tables(self):
        sql = SqlUtil.create_bak_table_sql(["t1", "t2"], bak_date="20240101")
        assert "t1_20240101" in sql
        assert "t2_20240101" in sql

    def test_length_mismatch(self):
        with pytest.raises(ValueError):
            SqlUtil.create_bak_table_sql(["t1", "t2"], bak_table=["bak1"])

    def test_default_date(self):
        sql = SqlUtil.create_bak_table_sql("user")
        # 应包含当天日期格式的备份表名
        today = datetime.datetime.now().strftime("%Y%m%d")
        assert f"user_{today}" in sql


class TestNumpyTypes:
    """numpy 类型测试（仅在安装了 numpy 时运行）"""

    def test_numpy_float(self):
        np = pytest.importorskip("numpy")
        sql = SqlUtil.make_insert_sql("user", {"score": np.float64(3.14)})
        assert "3.14" in sql

    def test_numpy_int(self):
        np = pytest.importorskip("numpy")
        sql = SqlUtil.make_insert_sql("user", {"count": np.int64(42)})
        assert "42" in sql

    def test_numpy_bool(self):
        np = pytest.importorskip("numpy")
        sql = SqlUtil.make_insert_sql("user", {"active": np.bool_(True)})
        # bool 判断在 numpy 之前，np.bool_ 作为 bool 子类也会被处理为 int(1)
        assert "1" in sql

    def test_numpy_float32(self):
        np = pytest.importorskip("numpy")
        val = SqlUtil._format_sql_value(np.float32(1.5))
        assert isinstance(val, float)
        assert val == 1.5

    def test_numpy_int8(self):
        np = pytest.importorskip("numpy")
        val = SqlUtil._format_sql_value(np.int8(7))
        assert isinstance(val, int)
        assert val == 7
