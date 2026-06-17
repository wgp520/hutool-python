from hutool import DataSizeUtil, FileNameUtil


class TestFileNameUtil:
    def test_get_name(self):
        assert FileNameUtil.get_name("/path/to/file.txt") == "file.txt"

    def test_get_prefix(self):
        assert FileNameUtil.get_prefix("/path/to/file.txt") == "file"

    def test_get_suffix(self):
        assert FileNameUtil.get_suffix("/path/to/file.txt") == "txt"

    def test_main_name(self):
        assert FileNameUtil.main_name("/path/to/file.txt") == "file"

    def test_ext_name(self):
        assert FileNameUtil.ext_name("/path/to/file.txt") == "txt"

    def test_clean_invalid(self):
        result = FileNameUtil.clean_invalid("file<name>.txt")
        assert "<" not in result
        assert ">" not in result

    def test_is_type(self):
        assert FileNameUtil.is_type("/path/to/file.txt", "txt") is True
        assert FileNameUtil.is_type("/path/to/file.txt", "py") is False


class TestDataSizeUtil:
    def test_parse(self):
        assert DataSizeUtil.parse("1KB") == 1024
        assert DataSizeUtil.parse("1MB") == 1048576
        assert DataSizeUtil.parse("1GB") == 1073741824
        assert DataSizeUtil.parse("1024B") == 1024

    def test_format(self):
        assert DataSizeUtil.format_size(1024) == "1KB"
        assert DataSizeUtil.format_size(1048576) == "1MB"

    def test_parse_case_insensitive(self):
        assert DataSizeUtil.parse("1kb") == 1024
        assert DataSizeUtil.parse("1Kb") == 1024

    def test_parse_zero(self):
        assert DataSizeUtil.parse("0B") == 0
