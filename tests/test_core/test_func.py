import math

from hutool import FuncUtil


class TestParseFunc:
    def test_math_sqrt(self):
        result = FuncUtil.parse_func("math.sqrt(2)")
        assert result is not None
        module, func_name, args, kwargs = result
        assert module == "math"
        assert func_name == "sqrt"
        assert args == [2]
        assert kwargs == {}

    def test_builtin_len(self):
        result = FuncUtil.parse_func("len([1, 2, 3])")
        assert result is not None
        module, func_name, args, _ = result
        assert module is None
        assert func_name == "len"
        assert args == [[1, 2, 3]]

    def test_kwargs(self):
        result = FuncUtil.parse_func("dict(a=1, b=2)")
        assert result is not None
        _, _, _, kwargs = result
        assert kwargs == {"a": 1, "b": 2}

    def test_nested_call(self):
        result = FuncUtil.parse_func("int(float('3.14'))")
        assert result is not None
        _, func_name, _, _ = result
        assert func_name == "int"

    def test_no_call(self):
        result = FuncUtil.parse_func("x + 1")
        assert result is None

    def test_dotted_module(self):
        result = FuncUtil.parse_func("os.path.join('a', 'b')")
        assert result is not None
        module, func_name, args, _ = result
        assert module == "os.path"
        assert func_name == "join"
        assert args == ["a", "b"]


class TestCallableFunc:
    def test_math_sqrt(self):
        fn = FuncUtil.callable_func("math.sqrt(2)")
        assert fn is not None
        assert fn() == math.sqrt(2)

    def test_with_extra_args(self):
        fn = FuncUtil.callable_func("math.pow(2)")
        assert fn is not None
        assert fn(10) == 2**10

    def test_invalid(self):
        fn = FuncUtil.callable_func("invalid!!!")
        assert fn is None


class TestCallFunc:
    def test_math_sqrt(self):
        result = FuncUtil.call_func("math.sqrt", 4)
        assert result == 2.0

    def test_len(self):
        result = FuncUtil.call_func("len", [1, 2, 3])
        assert result == 3

    def test_with_kwargs(self):
        result = FuncUtil.call_func("dict", a=1, b=2)
        assert result == {"a": 1, "b": 2}

    def test_nested(self):
        result = FuncUtil.call_func("int(float('3.14'))")
        assert result == 3


class TestSafeCall:
    def test_success(self):
        result = FuncUtil.safe_call("math.sqrt", 9)
        assert result == 3.0

    def test_failure_returns_default(self):
        result = FuncUtil.safe_call("nonexistent.func", default=-1)
        assert result == -1

    def test_none_default(self):
        result = FuncUtil.safe_call("invalid!!!")
        assert result is None


class TestIsCallable:
    def test_valid(self):
        assert FuncUtil.is_callable("math.sqrt(2)") is True

    def test_builtin(self):
        assert FuncUtil.is_callable("len([1])") is True

    def test_invalid(self):
        assert FuncUtil.is_callable("not a function") is False

    def test_syntax_error(self):
        assert FuncUtil.is_callable("(((") is False


class TestGetFuncName:
    def test_dotted(self):
        assert FuncUtil.get_func_name("math.sqrt(2)") == "sqrt"

    def test_nested_dotted(self):
        assert FuncUtil.get_func_name("datetime.datetime.now()") == "now"

    def test_simple(self):
        assert FuncUtil.get_func_name("len([1, 2])") == "len"

    def test_invalid(self):
        assert FuncUtil.get_func_name("not valid !!!") is None


class TestResolveFunc:
    def test_math_sqrt(self):
        fn = FuncUtil.resolve_func("math.sqrt")
        assert fn is math.sqrt

    def test_os_path_join(self):
        import os.path

        fn = FuncUtil.resolve_func("os.path.join")
        assert fn is os.path.join

    def test_nonexistent(self):
        assert FuncUtil.resolve_func("nonexistent.module.func") is None


class TestParseCall:
    def test_returns_tuple(self):
        result = FuncUtil.parse_func("math.sqrt(4)")
        assert result is not None
        module, func_name, args, kwargs = result
        assert module == "math"
        assert func_name == "sqrt"
        assert args == [4]
        assert kwargs == {}
