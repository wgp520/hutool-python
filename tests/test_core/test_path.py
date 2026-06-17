import os

import pytest

from hutool import PathUtil


class TestPathUtilNewMethods:
    def test_get_mime_type(self, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("hello", encoding="utf-8")
        assert PathUtil.get_mime_type(str(p)) == "text/plain"

    def test_is_dir_empty(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        assert PathUtil.is_dir_empty(str(d)) is True
        (d / "f.txt").touch()
        assert PathUtil.is_dir_empty(str(d)) is False

    def test_is_directory(self, tmp_path):
        d = tmp_path / "dir"
        d.mkdir()
        assert PathUtil.is_directory(str(d)) is True
        f = tmp_path / "file.txt"
        f.touch()
        assert PathUtil.is_directory(str(f)) is False

    def test_is_file(self, tmp_path):
        f = tmp_path / "file.txt"
        f.touch()
        assert PathUtil.is_file(str(f)) is True
        assert PathUtil.is_file(str(tmp_path)) is False

    def test_is_exists_and_not_directory(self, tmp_path):
        f = tmp_path / "f.txt"
        f.touch()
        assert PathUtil.is_exists_and_not_directory(str(f)) is True
        assert PathUtil.is_exists_and_not_directory(str(tmp_path)) is False

    def test_is_sub(self, tmp_path):
        parent = str(tmp_path)
        child = str(tmp_path / "sub" / "f.txt")
        assert PathUtil.is_sub(parent, child) is True
        assert PathUtil.is_sub(child, parent) is False

    def test_is_symlink(self, tmp_path):
        target = tmp_path / "target.txt"
        target.write_text("data", encoding="utf-8")
        link = tmp_path / "link.txt"
        try:
            link.symlink_to(target)
            assert PathUtil.is_symlink(str(link)) is True
        except OSError:
            pytest.skip("Cannot create symlink")

    def test_get_path_ele(self):
        parts = PathUtil.get_path_ele("/a/b/c", 0)
        assert parts is not None

    def test_get_last_path_ele(self):
        assert PathUtil.get_last_path_ele("/a/b/c.txt") == "c.txt"

    def test_rename_path(self, tmp_path):
        f = tmp_path / "old.txt"
        f.write_text("data", encoding="utf-8")
        new_p = PathUtil.rename_path(str(f), "new.txt")
        assert PathUtil.exists(new_p)

    def test_to_abs_normal(self):
        result = PathUtil.to_abs_normal(".")
        assert os.path.isabs(result)

    def test_create_temp_file(self, tmp_path):
        p = PathUtil.create_temp_file(dir_path=str(tmp_path))
        assert p.exists()

    def test_walk_files(self, tmp_path):
        (tmp_path / "a.txt").write_text("a", encoding="utf-8")
        (tmp_path / "b.txt").write_text("b", encoding="utf-8")
        files = list(PathUtil.walk_files(str(tmp_path)))
        assert len(files) >= 2

    def test_copy_file(self, tmp_path):
        src = tmp_path / "src.txt"
        dest = tmp_path / "dest.txt"
        src.write_text("data", encoding="utf-8")
        PathUtil.copy_file(str(src), str(dest))
        assert dest.exists()
