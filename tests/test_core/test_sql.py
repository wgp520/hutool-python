"""SqlUtil 测试"""

import datetime

import pytest

from hutool import SqlUtil
from hutool.core.sql import ColumnType, F, Q


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


# ── PostgreSQL 方言测试 ──────────────────────────────────────────


class TestPostgresqlDialect:
    def test_select_double_quotes(self):
        """PostgreSQL 标识符使用双引号。"""
        sql = SqlUtil.make_select_sql("user", ["name", "age"], dialect="postgresql")
        assert sql == 'SELECT "name","age" FROM "user"'

    def test_select_pagination(self):
        """PostgreSQL 使用 LIMIT ... OFFSET ... 语法。"""
        sql = SqlUtil.make_select_sql("user", "*", page_no=2, page_size=10, dialect="postgresql")
        assert sql == 'SELECT * FROM "user" LIMIT 10 OFFSET 10'

    def test_select_page_no_less_than_1(self):
        sql = SqlUtil.make_select_sql("user", "*", page_no=0, page_size=10, dialect="postgresql")
        assert "LIMIT 10 OFFSET 0" in sql

    def test_select_full(self):
        sql = SqlUtil.make_select_sql(
            "user",
            ["id", "name"],
            condition="age > 18",
            order_by=["id"],
            page_no=1,
            page_size=5,
            dialect="postgresql",
        )
        assert 'SELECT "id","name" FROM "user"' in sql
        assert "WHERE age > 18" in sql
        assert 'ORDER BY "id"' in sql
        assert "LIMIT 5 OFFSET 0" in sql

    def test_insert_ignore(self):
        """PostgreSQL INSERT IGNORE 转为 ON CONFLICT DO NOTHING。"""
        sql = SqlUtil.make_insert_sql("user", {"name": "Alice"}, insert_ignore=True, dialect="postgresql")
        assert "ON CONFLICT DO NOTHING" in sql
        assert "INSERT INTO" in sql
        assert "VALUES" in sql

    def test_update_columns(self):
        """PostgreSQL ON DUPLICATE KEY UPDATE 转为 ON CONFLICT DO UPDATE SET。"""
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice", "age": 20},
            update_columns=("name",),
            on_conflict=("id",),
            dialect="postgresql",
        )
        assert 'ON CONFLICT (id) DO UPDATE SET "name"=EXCLUDED."name"' in sql
        assert 'INSERT INTO "user"' in sql

    def test_update_columns_with_values(self):
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice"},
            update_columns=("name",),
            update_columns_value=("'Bob'",),
            on_conflict=("id",),
            dialect="postgresql",
        )
        assert "ON CONFLICT (id) DO UPDATE SET \"name\"='Bob'" in sql

    def test_auto_update_with_conflict(self):
        """PostgreSQL auto_update 需要 on_conflict，替换所有字段。"""
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice", "age": 20},
            auto_update=True,
            on_conflict=("id",),
            dialect="postgresql",
        )
        assert "ON CONFLICT (id) DO UPDATE SET" in sql
        assert 'EXCLUDED."name"' in sql
        assert 'EXCLUDED."age"' in sql

    def test_auto_update_without_conflict_raises(self):
        """PostgreSQL auto_update 无 on_conflict 时应抛出 ValueError。"""
        with pytest.raises(ValueError, match="on_conflict"):
            SqlUtil.make_insert_sql("user", {"name": "Alice"}, auto_update=True, dialect="postgresql")

    def test_update_columns_default_conflict(self):
        """update_columns 未指定 on_conflict 时，使用 update_columns 作为冲突列。"""
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice", "age": 20},
            update_columns=("name",),
            dialect="postgresql",
        )
        assert "ON CONFLICT (name) DO UPDATE SET" in sql

    def test_update_sql(self):
        """PostgreSQL 更新语句使用双引号。"""
        sql = SqlUtil.make_update_sql("user", {"name": "Bob"}, "id = 1", dialect="postgresql")
        assert 'UPDATE "user" SET' in sql
        assert '"name"' in sql
        assert "WHERE id = 1" in sql

    def test_delete_sql(self):
        """PostgreSQL 删除语句与方言无关（无标识符引用）。"""
        sql = SqlUtil.make_delete_sql("user", "id = 1", dialect="postgresql")
        assert sql == "DELETE FROM user WHERE id = 1"


# ── SQLite 方言测试 ─────────────────────────────────────────────


class TestSqliteDialect:
    def test_select_backtick_quotes(self):
        """SQLite 标识符使用反引号（与 MySQL 相同）。"""
        sql = SqlUtil.make_select_sql("user", ["name", "age"], dialect="sqlite")
        assert sql == "SELECT `name`,`age` FROM `user`"

    def test_select_pagination(self):
        """SQLite 使用 LIMIT ... OFFSET ... 语法。"""
        sql = SqlUtil.make_select_sql("user", "*", page_no=2, page_size=10, dialect="sqlite")
        assert sql == "SELECT * FROM `user` LIMIT 10 OFFSET 10"

    def test_insert_ignore(self):
        """SQLite INSERT IGNORE 转为 INSERT OR IGNORE。"""
        sql = SqlUtil.make_insert_sql("user", {"name": "Alice"}, insert_ignore=True, dialect="sqlite")
        assert "INSERT OR IGNORE INTO" in sql

    def test_replace_into(self):
        """SQLite auto_update 转为 INSERT OR REPLACE。"""
        sql = SqlUtil.make_insert_sql("user", {"name": "Alice"}, auto_update=True, dialect="sqlite")
        assert "INSERT OR REPLACE INTO" in sql

    def test_update_columns(self):
        """SQLite ON DUPLICATE KEY UPDATE 转为 ON CONFLICT DO UPDATE SET（excluded 小写）。"""
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice", "age": 20},
            update_columns=("name",),
            on_conflict=("id",),
            dialect="sqlite",
        )
        assert "ON CONFLICT (id) DO UPDATE SET" in sql
        assert "`name`=excluded.`name`" in sql

    def test_update_columns_with_values(self):
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice"},
            update_columns=("name",),
            update_columns_value=("'Bob'",),
            on_conflict=("id",),
            dialect="sqlite",
        )
        assert "`name`='Bob'" in sql
        assert "ON CONFLICT (id)" in sql

    def test_update_columns_default_conflict(self):
        """update_columns 未指定 on_conflict 时，使用 update_columns 作为冲突列。"""
        sql = SqlUtil.make_insert_sql(
            "user",
            {"name": "Alice", "age": 20},
            update_columns=("name",),
            dialect="sqlite",
        )
        assert "ON CONFLICT (name) DO UPDATE SET" in sql

    def test_update_sql(self):
        """SQLite 更新语句使用反引号（与 MySQL 相同）。"""
        sql = SqlUtil.make_update_sql("user", {"name": "Bob"}, "id = 1", dialect="sqlite")
        assert "UPDATE `user` SET" in sql
        assert "`name`=" in sql
        assert "WHERE id = 1" in sql

    def test_delete_sql(self):
        sql = SqlUtil.make_delete_sql("user", "id = 1", dialect="sqlite")
        assert sql == "DELETE FROM user WHERE id = 1"

    def test_create_bak_table(self):
        sql = SqlUtil.create_bak_table_sql("user", bak_date="20240101", dialect="sqlite")
        assert "create table user_20240101 as select * from user" in sql

    def test_none_values_become_null(self):
        sql = SqlUtil.make_insert_sql("user", {"name": None}, dialect="sqlite")
        assert "null" in sql


# ── 方言校验测试 ────────────────────────────────────────────────


class TestDialectValidation:
    def test_invalid_dialect_select(self):
        with pytest.raises(ValueError, match="不支持的方言"):
            SqlUtil.make_select_sql("user", "*", dialect="oracle")

    def test_invalid_dialect_insert(self):
        with pytest.raises(ValueError, match="不支持的方言"):
            SqlUtil.make_insert_sql("user", {"name": "A"}, dialect="sqlserver")

    def test_invalid_dialect_update(self):
        with pytest.raises(ValueError, match="不支持的方言"):
            SqlUtil.make_update_sql("user", {"name": "A"}, "id = 1", dialect="mssql")

    def test_invalid_dialect_delete(self):
        with pytest.raises(ValueError, match="不支持的方言"):
            SqlUtil.make_delete_sql("user", "id = 1", dialect="firebird")

    def test_invalid_dialect_bak_table(self):
        with pytest.raises(ValueError, match="不支持的方言"):
            SqlUtil.create_bak_table_sql("user", dialect="db2")

    def test_mysql_is_default(self):
        """默认方言应为 MySQL。"""
        sql = SqlUtil.make_select_sql("user", ["name"])
        assert "`name`" in sql
        assert "`user`" in sql


# ═══════════════════════════════════════════════════════════════════
# 链式调用 API 测试
# ═══════════════════════════════════════════════════════════════════


# ── Q 条件组合器 ──────────────────────────────────────────────


class TestQ:
    def test_simple_eq(self):
        q = Q(name="Alice")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert sql == "`name`='Alice'"

    def test_gt(self):
        q = Q(age__gt=18)
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert sql == "`age`>18"

    def test_in(self):
        q = Q(status__in=["active", "pending"])
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "IN" in sql
        assert "active" in sql
        assert "pending" in sql

    def test_isnull_true(self):
        q = Q(deleted_at__isnull=True)
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "IS NULL" in sql

    def test_isnull_false(self):
        q = Q(deleted_at__isnull=False)
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "IS NOT NULL" in sql

    def test_contains(self):
        q = Q(name__contains="test")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "LIKE '%test%'" in sql

    def test_startswith(self):
        q = Q(name__startswith="A")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "LIKE 'A%'" in sql

    def test_endswith(self):
        q = Q(name__endswith="z")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "LIKE '%z'" in sql

    def test_between(self):
        q = Q(age__between=(18, 65))
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "BETWEEN 18 AND 65" in sql

    def test_or(self):
        q = Q(age__gt=18) | Q(role="admin")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "OR" in sql
        assert "`age`>18" in sql
        assert "`role`='admin'" in sql

    def test_and(self):
        q = Q(age__gt=18) & Q(status="active")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "AND" in sql

    def test_invert(self):
        q = ~Q(status="deleted")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "NOT" in sql

    def test_complex_nesting(self):
        q = (Q(age__gte=18, status="active") | Q(role="admin")) & Q(dept__in=["IT", "HR"])
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "mysql")
        assert "OR" in sql
        assert "AND" in sql
        assert "IN" in sql

    def test_postgresql_quotes(self):
        q = Q(name="Alice")
        sql = q.to_sql(SqlUtil._quote, SqlUtil._format_sql_value, "postgresql")
        assert sql == "\"name\"='Alice'"


# ── F 字段引用 ────────────────────────────────────────────────


class TestF:
    def test_simple_field(self):
        f = F("balance")
        assert f.to_sql(SqlUtil._quote, "mysql") == "`balance`"

    def test_add(self):
        f = F("balance") + 100
        assert f.to_sql(SqlUtil._quote, "mysql") == "`balance`+100"

    def test_sub(self):
        f = F("stock") - 10
        assert f.to_sql(SqlUtil._quote, "mysql") == "`stock`-10"

    def test_mul(self):
        f = F("price") * 1.5
        assert f.to_sql(SqlUtil._quote, "mysql") == "`price`*1.5"

    def test_div(self):
        f = F("total") / 2
        assert f.to_sql(SqlUtil._quote, "mysql") == "`total`/2"

    def test_neg(self):
        f = -F("score")
        assert f.to_sql(SqlUtil._quote, "mysql") == "-`score`"

    def test_count(self):
        f = F.count("*")
        assert f.to_sql(SqlUtil._quote, "mysql") == "COUNT(*)"

    def test_count_field(self):
        f = F.count("id")
        assert f.to_sql(SqlUtil._quote, "mysql") == "COUNT(`id`)"

    def test_sum(self):
        f = F.sum("amount")
        assert f.to_sql(SqlUtil._quote, "mysql") == "SUM(`amount`)"

    def test_avg(self):
        f = F.avg("score")
        assert f.to_sql(SqlUtil._quote, "mysql") == "AVG(`score`)"

    def test_max(self):
        f = F.max("price")
        assert f.to_sql(SqlUtil._quote, "mysql") == "MAX(`price`)"

    def test_min(self):
        f = F.min("price")
        assert f.to_sql(SqlUtil._quote, "mysql") == "MIN(`price`)"

    def test_postgresql_quotes(self):
        f = F("balance")
        assert f.to_sql(SqlUtil._quote, "postgresql") == '"balance"'

    def test_complex_expression(self):
        f = F("cost") * 1.5 + 10
        sql = f.to_sql(SqlUtil._quote, "mysql")
        assert sql == "`cost`*1.5+10"


# ── ColumnType 枚举 ──────────────────────────────────────────


class TestColumnType:
    def test_varchar_mysql(self):
        assert ColumnType.VARCHAR.to_sql("mysql", "(100)") == "VARCHAR(100)"

    def test_varchar_postgresql(self):
        assert ColumnType.VARCHAR.to_sql("postgresql", "(100)") == "VARCHAR(100)"

    def test_varchar_sqlite(self):
        assert ColumnType.VARCHAR.to_sql("sqlite", "(100)") == "TEXT(100)"

    def test_serial_mysql(self):
        assert ColumnType.SERIAL.to_sql("mysql") == "INT AUTO_INCREMENT"

    def test_serial_postgresql(self):
        assert ColumnType.SERIAL.to_sql("postgresql") == "SERIAL"

    def test_serial_sqlite(self):
        assert ColumnType.SERIAL.to_sql("sqlite") == "INTEGER"

    def test_boolean_mysql(self):
        assert ColumnType.BOOLEAN.to_sql("mysql") == "TINYINT(1)"

    def test_boolean_postgresql(self):
        assert ColumnType.BOOLEAN.to_sql("postgresql") == "BOOLEAN"

    def test_boolean_sqlite(self):
        assert ColumnType.BOOLEAN.to_sql("sqlite") == "INTEGER"

    def test_json_mysql(self):
        assert ColumnType.JSON.to_sql("mysql") == "JSON"

    def test_json_postgresql(self):
        assert ColumnType.JSON.to_sql("postgresql") == "JSONB"

    def test_json_sqlite(self):
        assert ColumnType.JSON.to_sql("sqlite") == "TEXT"

    def test_uuid_mysql(self):
        assert ColumnType.UUID.to_sql("mysql") == "CHAR(36)"

    def test_uuid_postgresql(self):
        assert ColumnType.UUID.to_sql("postgresql") == "UUID"

    def test_uuid_sqlite(self):
        assert ColumnType.UUID.to_sql("sqlite") == "TEXT"

    def test_int_no_args(self):
        assert ColumnType.INT.to_sql("mysql") == "INT"

    def test_decimal_with_args(self):
        assert ColumnType.DECIMAL.to_sql("mysql", "(10,2)") == "DECIMAL(10,2)"

    def test_datetime_postgresql(self):
        assert ColumnType.DATETIME.to_sql("postgresql") == "TIMESTAMP"

    def test_blob_postgresql(self):
        assert ColumnType.BLOB.to_sql("postgresql") == "BYTEA"


# ── SelectBuilder ─────────────────────────────────────────────


class TestSelectBuilder:
    def test_basic(self):
        sql = SqlUtil.select("user").columns("id", "name").sql()
        assert sql == "SELECT `id`, `name` FROM `user`"

    def test_select_star(self):
        sql = SqlUtil.select("user").sql()
        assert sql == "SELECT * FROM `user`"

    def test_where_kwargs(self):
        sql = SqlUtil.select("user").columns("*").where(age__gt=18).sql()
        assert "`age`>18" in sql
        assert "WHERE" in sql

    def test_where_q(self):
        sql = SqlUtil.select("user").where(Q(age__gt=18) | Q(role="admin")).sql()
        assert "OR" in sql
        assert "`age`>18" in sql

    def test_where_raw(self):
        sql = SqlUtil.select("user").where_raw("find_in_set(1, status)").sql()
        assert "find_in_set(1, status)" in sql

    def test_order_by_asc(self):
        sql = SqlUtil.select("user").columns("*").order_by("name").sql()
        assert "ORDER BY `name` ASC" in sql

    def test_order_by_desc(self):
        sql = SqlUtil.select("user").columns("*").order_by("-age").sql()
        assert "ORDER BY `age` DESC" in sql

    def test_order_by_raw(self):
        sql = SqlUtil.select("user").columns("*").order_by("FIELD(status, 'vip')").sql()
        assert "FIELD(status, 'vip')" in sql

    def test_limit(self):
        sql = SqlUtil.select("user").columns("*").limit(10).sql()
        assert "LIMIT" in sql

    def test_offset(self):
        sql = SqlUtil.select("user").columns("*").limit(10).offset(20).sql()
        assert "LIMIT" in sql
        assert "20" in sql

    def test_page(self):
        sql = SqlUtil.select("user").columns("*").page(2, 10).sql()
        assert "LIMIT" in sql

    def test_distinct(self):
        sql = SqlUtil.select("user").columns("name").distinct().sql()
        assert "SELECT DISTINCT" in sql

    def test_group_by(self):
        sql = SqlUtil.select("order").columns("user_id", "COUNT(*) AS cnt").group_by("user_id").sql()
        assert "GROUP BY `user_id`" in sql

    def test_having(self):
        sql = SqlUtil.select("order").columns("user_id", "COUNT(*) AS cnt").group_by("user_id").having(cnt__gt=5).sql()
        assert "HAVING" in sql

    def test_columns_raw_expression(self):
        sql = (
            SqlUtil.select(
                "user",
            )
            .columns("id", "COUNT(*) AS cnt")
            .group_by("id")
            .sql()
        )
        assert "COUNT(*) AS cnt" in sql

    def test_postgresql(self):
        sql = SqlUtil.select("user", dialect="postgresql").columns("id", "name").where(id=1).sql()
        assert '"id"' in sql
        assert '"name"' in sql
        assert '"user"' in sql

    def test_postgresql_pagination(self):
        sql = SqlUtil.select("user", dialect="postgresql").columns("*").page(2, 10).sql()
        assert "LIMIT 10 OFFSET 10" in sql

    def test_sqlite(self):
        sql = SqlUtil.select("user", dialect="sqlite").columns("name").sql()
        assert "`name`" in sql

    def test_where_raw_string(self):
        """where 中传入原始 SQL 字符串。"""
        sql = SqlUtil.select("user").where("YEAR(created_at) = 2024").sql()
        assert "YEAR(created_at) = 2024" in sql

    def test_f_field_in_where(self):
        """F() 用于 where 条件。"""
        sql = SqlUtil.select("product").where(price__gt=F("cost") * 1.5).sql()
        assert "`price`>`cost`*1.5" in sql


# ── InsertBuilder ─────────────────────────────────────────────


class TestInsertBuilder:
    def test_basic(self):
        sql = SqlUtil.insert("user").values(name="Alice", age=20).sql()
        assert "INSERT INTO" in sql
        assert "Alice" in sql
        assert "20" in sql

    def test_batch(self):
        data = [{"name": "Alice", "age": 20}, {"name": "Bob", "age": 30}]
        sql = SqlUtil.insert("user").values_list(data).sql()
        assert "Alice" in sql
        assert "Bob" in sql

    def test_ignore_mysql(self):
        sql = SqlUtil.insert("user").values(name="Alice").ignore().sql()
        assert "INSERT ignore INTO" in sql

    def test_replace_mysql(self):
        sql = SqlUtil.insert("user").values(name="Alice").replace().sql()
        assert "REPLACE INTO" in sql

    def test_on_duplicate_key_mysql(self):
        sql = SqlUtil.insert("user").values(name="Alice", age=20).do_update("name").sql()
        assert "ON DUPLICATE KEY UPDATE" in sql
        assert "`name`=VALUES(`name`)" in sql

    def test_on_conflict_pg(self):
        sql = (
            SqlUtil.insert("user", dialect="postgresql")
            .values(name="Alice", age=20)
            .on_conflict("id")
            .do_update("name", "age")
            .sql()
        )
        assert "ON CONFLICT (id) DO UPDATE SET" in sql
        assert "EXCLUDED" in sql

    def test_on_conflict_sqlite(self):
        sql = (
            SqlUtil.insert("user", dialect="sqlite")
            .values(name="Alice", age=20)
            .on_conflict("id")
            .do_update("name")
            .sql()
        )
        assert "ON CONFLICT (id) DO UPDATE SET" in sql
        assert "excluded" in sql

    def test_do_nothing_pg(self):
        sql = SqlUtil.insert("user", dialect="postgresql").values(name="Alice").do_nothing().sql()
        assert "ON CONFLICT DO NOTHING" in sql

    def test_do_nothing_sqlite(self):
        sql = SqlUtil.insert("user", dialect="sqlite").values(name="Alice").do_nothing().sql()
        assert "INSERT OR IGNORE INTO" in sql

    def test_none_values_become_null(self):
        sql = SqlUtil.insert("user").values(name=None).sql()
        assert "null" in sql

    def test_empty_data(self):
        assert SqlUtil.insert("user").sql() == ""

    def test_postgresql_quotes(self):
        sql = SqlUtil.insert("user", dialect="postgresql").values(name="Alice").sql()
        assert '"user"' in sql
        assert '"name"' in sql


# ── UpdateBuilder ─────────────────────────────────────────────


class TestUpdateBuilder:
    def test_basic(self):
        sql = SqlUtil.update("user").set(name="Bob").where(id=1).sql()
        assert "UPDATE `user` SET" in sql
        assert "`name`='Bob'" in sql
        assert "`id`=1" in sql

    def test_multiple_fields(self):
        sql = SqlUtil.update("user").set(name="Bob", age=30).where(id=1).sql()
        assert "`name`=" in sql
        assert "`age`=30" in sql

    def test_f_field(self):
        sql = SqlUtil.update("account").set(balance=F("balance") + 100).where(id=1).sql()
        assert "`balance`=`balance`+100" in sql

    def test_set_raw(self):
        sql = SqlUtil.update("account").set_raw("balance = balance + 100").where(id=1).sql()
        assert "balance = balance + 100" in sql

    def test_where_q(self):
        sql = SqlUtil.update("user").set(active=False).where(Q(status="banned") | Q(inactive_days__gt=365)).sql()
        assert "OR" in sql

    def test_where_raw(self):
        sql = SqlUtil.update("user").set(active=False).where_raw("login_count > 100").sql()
        assert "login_count > 100" in sql

    def test_postgresql(self):
        sql = SqlUtil.update("user", dialect="postgresql").set(name="Bob").where(id=1).sql()
        assert '"user"' in sql
        assert '"name"' in sql

    def test_none_value(self):
        sql = SqlUtil.update("user").set(name=None).where(id=1).sql()
        assert "null" in sql


# ── DeleteBuilder ─────────────────────────────────────────────


class TestDeleteBuilder:
    def test_basic(self):
        sql = SqlUtil.delete("user").where(id=1).sql()
        assert sql == "DELETE FROM `user` WHERE `id`=1"

    def test_multiple_conditions(self):
        sql = SqlUtil.delete("user").where(status="inactive", created_at__lt="2020-01-01").sql()
        assert "`status`='inactive'" in sql
        assert "`created_at`<'2020-01-01'" in sql

    def test_where_q(self):
        sql = SqlUtil.delete("user").where(Q(age__lt=18) | Q(status="banned")).sql()
        assert "OR" in sql

    def test_where_raw(self):
        sql = SqlUtil.delete("user").where_raw("DATEDIFF(NOW(), created_at) > 365").sql()
        assert "DATEDIFF" in sql

    def test_no_where(self):
        sql = SqlUtil.delete("user").sql()
        assert sql == "DELETE FROM `user`"

    def test_postgresql(self):
        sql = SqlUtil.delete("user", dialect="postgresql").where(id=1).sql()
        assert '"user"' in sql
        assert '"id"' in sql


# ── CreateTableBuilder ────────────────────────────────────────


class TestCreateTableBuilder:
    def test_basic(self):
        sql = (
            SqlUtil.create_table("user")
            .column("id", ColumnType.INT, primary_key=True)
            .column("name", ColumnType.VARCHAR, type_args="(100)", nullable=False)
            .column("age", ColumnType.INT, default=0)
            .sql()
        )
        assert "CREATE TABLE" in sql
        assert "`id` INT PRIMARY KEY" in sql
        assert "`name` VARCHAR(100) NOT NULL" in sql
        assert "`age` INT DEFAULT 0" in sql

    def test_if_not_exists(self):
        sql = SqlUtil.create_table("user").column("id", ColumnType.INT).if_not_exists().sql()
        assert "IF NOT EXISTS" in sql

    def test_serial_mysql(self):
        sql = SqlUtil.create_table("user").column("id", ColumnType.SERIAL, primary_key=True).sql()
        assert "INT AUTO_INCREMENT PRIMARY KEY" in sql

    def test_serial_postgresql(self):
        sql = SqlUtil.create_table("user", dialect="postgresql").column("id", ColumnType.SERIAL, primary_key=True).sql()
        assert "SERIAL PRIMARY KEY" in sql

    def test_boolean_mysql(self):
        sql = SqlUtil.create_table("user").column("active", ColumnType.BOOLEAN, default=True).sql()
        assert "TINYINT(1)" in sql
        assert "DEFAULT true" in sql

    def test_boolean_postgresql(self):
        sql = SqlUtil.create_table("user", dialect="postgresql").column("active", ColumnType.BOOLEAN).sql()
        assert "BOOLEAN" in sql

    def test_json_mysql(self):
        sql = SqlUtil.create_table("user").column("extra", ColumnType.JSON).sql()
        assert "JSON" in sql

    def test_json_postgresql(self):
        sql = SqlUtil.create_table("user", dialect="postgresql").column("extra", ColumnType.JSON).sql()
        assert "JSONB" in sql

    def test_json_sqlite(self):
        sql = SqlUtil.create_table("user", dialect="sqlite").column("extra", ColumnType.JSON).sql()
        assert "TEXT" in sql

    def test_uuid_postgresql(self):
        sql = SqlUtil.create_table("user", dialect="postgresql").column("uid", ColumnType.UUID).sql()
        assert "UUID" in sql

    def test_composite_primary_key(self):
        sql = (
            SqlUtil.create_table("user_role")
            .column("user_id", ColumnType.INT)
            .column("role_id", ColumnType.INT)
            .primary_key("user_id", "role_id")
            .sql()
        )
        assert "PRIMARY KEY (`user_id`, `role_id`)" in sql

    def test_engine_charset_mysql(self):
        sql = SqlUtil.create_table("user").column("id", ColumnType.INT).engine("InnoDB").charset("utf8mb4").sql()
        assert "ENGINE=InnoDB" in sql
        assert "DEFAULT CHARSET=utf8mb4" in sql

    def test_unique(self):
        sql = SqlUtil.create_table("user").column("email", ColumnType.VARCHAR, type_args="(255)", unique=True).sql()
        assert "UNIQUE" in sql

    def test_auto_increment(self):
        sql = SqlUtil.create_table("user").column("id", ColumnType.BIGINT, auto_increment=True).sql()
        assert "AUTO_INCREMENT" in sql

    def test_comment_mysql(self):
        sql = SqlUtil.create_table("user").column("name", ColumnType.VARCHAR, type_args="(100)", comment="姓名").sql()
        assert "COMMENT '姓名'" in sql

    def test_postgresql_no_comment(self):
        sql = (
            SqlUtil.create_table("user", dialect="postgresql")
            .column("name", ColumnType.VARCHAR, type_args="(100)", comment="姓名")
            .sql()
        )
        assert "COMMENT" not in sql

    def test_default_string_value(self):
        sql = (
            SqlUtil.create_table("user").column("status", ColumnType.VARCHAR, type_args="(20)", default="active").sql()
        )
        assert "DEFAULT 'active'" in sql
