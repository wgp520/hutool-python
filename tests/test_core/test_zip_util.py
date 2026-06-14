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
