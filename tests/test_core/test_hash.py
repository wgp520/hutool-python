from hutool import HashUtil


class TestHashUtil:
    def test_java_hash_code(self):
        assert HashUtil.java_hash_code("test") == 3556498

    def test_java_hash_code_empty(self):
        assert HashUtil.java_hash_code("") == 0

    def test_bkdr_hash(self):
        result = HashUtil.bkdr_hash("test")
        assert isinstance(result, int)

    def test_ap_hash(self):
        result = HashUtil.ap_hash("test")
        assert isinstance(result, int)

    def test_djb_hash(self):
        result = HashUtil.djb_hash("test")
        assert isinstance(result, int)

    def test_js_hash(self):
        result = HashUtil.js_hash("test")
        assert isinstance(result, int)

    def test_rs_hash(self):
        result = HashUtil.rs_hash("test")
        assert isinstance(result, int)

    def test_sdbm_hash(self):
        result = HashUtil.sdbm_hash("test")
        assert isinstance(result, int)

    def test_elf_hash(self):
        result = HashUtil.elf_hash("test")
        assert isinstance(result, int)

    def test_fnv1(self):
        result = HashUtil.fnv1(b"test")
        assert isinstance(result, int)
        assert result > 0

    def test_fnv1a(self):
        result = HashUtil.fnv1a(b"test")
        assert isinstance(result, int)
        assert result > 0

    def test_dek_hash(self):
        result = HashUtil.dek_hash("test")
        assert isinstance(result, int)

    def test_bp_hash(self):
        result = HashUtil.bp_hash("test")
        assert isinstance(result, int)

    def test_pjw_hash(self):
        result = HashUtil.pjw_hash("test")
        assert isinstance(result, int)
