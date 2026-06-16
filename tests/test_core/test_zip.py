import os
import tempfile

from hutool import ZipUtil


class TestZipUtil:
    def test_gzip_and_ungzip(self):
        original = b"Hello, World!"
        compressed = ZipUtil.gzip(original)
        assert isinstance(compressed, bytes)
        assert compressed != original
        decompressed = ZipUtil.ungzip(compressed)
        assert decompressed == original

    def test_gzip_string(self):
        compressed = ZipUtil.gzip_str("hello")
        result = ZipUtil.ungzip_str(compressed)
        assert result == "hello"

    def test_zlib_and_unzlib(self):
        original = b"Hello, World!"
        compressed = ZipUtil.zlib_compress(original)
        assert isinstance(compressed, bytes)
        decompressed = ZipUtil.zlib_uncompress(compressed)
        assert decompressed == original

    def test_zip_and_unzip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "test.txt")
            with open(src, "w") as f:
                f.write("Hello, World!")

            zip_path = os.path.join(tmpdir, "test.zip")
            ZipUtil.zip(src, zip_path)
            assert os.path.exists(zip_path)

            dest = os.path.join(tmpdir, "extracted")
            os.makedirs(dest)
            ZipUtil.unzip(zip_path, dest)
            assert os.path.exists(os.path.join(dest, "test.txt"))
            with open(os.path.join(dest, "test.txt")) as f:
                assert f.read() == "Hello, World!"

    def test_zip_to_stream(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "test.txt")
            with open(src, "w") as f:
                f.write("data")
            data = ZipUtil.zip_to_stream(src)
            assert isinstance(data, bytes)
            assert len(data) > 0

    def test_zip_entries(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "test.txt")
            with open(src, "w") as f:
                f.write("data")
            zip_path = os.path.join(tmpdir, "out.zip")
            entries = ZipUtil.zip_entries(src, zip_path)
            assert "test.txt" in entries

    def test_list_file_names(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "test.txt")
            with open(src, "w") as f:
                f.write("data")
            zip_path = os.path.join(tmpdir, "out.zip")
            ZipUtil.zip(src, zip_path)
            names = ZipUtil.list_file_names(zip_path)
            assert "test.txt" in names

    def test_read_zip_entry(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "test.txt")
            with open(src, "w") as f:
                f.write("hello")
            zip_path = os.path.join(tmpdir, "out.zip")
            ZipUtil.zip(src, zip_path)
            content = ZipUtil.read(zip_path, "test.txt")
            assert content == b"hello"

    def test_unzip_stream(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "test.txt")
            with open(src, "w") as f:
                f.write("stream test")
            zip_data = ZipUtil.zip_to_stream(src)
            dest = os.path.join(tmpdir, "extracted")
            ZipUtil.unzip_stream(zip_data, dest)
            assert os.path.exists(os.path.join(dest, "test.txt"))

    def test_append(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            f1 = os.path.join(tmpdir, "a.txt")
            f2 = os.path.join(tmpdir, "b.txt")
            with open(f1, "w") as f:
                f.write("a")
            with open(f2, "w") as f:
                f.write("b")
            zip_path = os.path.join(tmpdir, "out.zip")
            ZipUtil.zip(f1, zip_path)
            ZipUtil.append(zip_path, f2)
            names = ZipUtil.list_file_names(zip_path)
            assert "a.txt" in names
            assert "b.txt" in names
