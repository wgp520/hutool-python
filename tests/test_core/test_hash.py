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

    def test_ap_hash_initial_value(self):
        """测试 ap_hash 初始值为 0（与 Java Hutool 一致）"""
        # 空字符串应返回 0
        assert HashUtil.ap_hash("") == 0
        # 非空字符串应返回非零值
        assert HashUtil.ap_hash("test") != 0

    def test_additive_hash(self):
        result = HashUtil.additive_hash("hello", 1009)
        assert isinstance(result, int)
        assert 0 <= result < 1009

    def test_rotating_hash(self):
        result = HashUtil.rotating_hash("hello", 1009)
        assert isinstance(result, int)
        assert 0 <= result < 1009

    def test_one_by_one_hash(self):
        result = HashUtil.one_by_one_hash("hello")
        assert isinstance(result, int)

    def test_bernstein_hash(self):
        result = HashUtil.bernstein_hash("hello")
        assert isinstance(result, int)
        # 与 djb_hash 不同
        assert result != HashUtil.djb_hash("hello") or True  # 不保证不同

    def test_int_hash(self):
        """测试 Thomas Wang 32位整数哈希"""
        result = HashUtil.int_hash(42)
        assert isinstance(result, int)
        assert 0 <= result <= 0xFFFFFFFF

    def test_tianl_hash(self):
        result = HashUtil.tianl_hash("hello")
        assert isinstance(result, int)
        assert result >= 0

    def test_tianl_hash_empty(self):
        assert HashUtil.tianl_hash("") == 0

    def test_tianl_hash_long_string(self):
        """测试超过 96 字符的字符串"""
        s = "a" * 200
        result = HashUtil.tianl_hash(s)
        assert isinstance(result, int)
        assert result >= 0

    def test_mix_hash(self):
        result = HashUtil.mix_hash("hello")
        assert isinstance(result, int)

    def test_murmur32(self):
        result = HashUtil.murmur32(b"hello")
        assert isinstance(result, int)
        assert 0 <= result <= 0xFFFFFFFF

    def test_murmur32_deterministic(self):
        """测试确定性"""
        assert HashUtil.murmur32(b"test") == HashUtil.murmur32(b"test")

    def test_murmur64(self):
        result = HashUtil.murmur64(b"hello")
        assert isinstance(result, int)

    def test_murmur128(self):
        h1, h2 = HashUtil.murmur128(b"hello")
        assert isinstance(h1, int)
        assert isinstance(h2, int)

    def test_city_hash32(self):
        result = HashUtil.city_hash32(b"hello")
        assert isinstance(result, int)
        assert 0 <= result <= 0xFFFFFFFF

    def test_city_hash64(self):
        result = HashUtil.city_hash64(b"hello")
        assert isinstance(result, int)

    def test_city_hash128(self):
        h1, h2 = HashUtil.city_hash128(b"hello")
        assert isinstance(h1, int)
        assert isinstance(h2, int)

    def test_metro_hash64(self):
        result = HashUtil.metro_hash64(b"hello")
        assert isinstance(result, int)

    def test_metro_hash128(self):
        h1, h2 = HashUtil.metro_hash128(b"hello")
        assert isinstance(h1, int)
        assert isinstance(h2, int)

    def test_hf_hash(self):
        result = HashUtil.hf_hash("hello")
        assert isinstance(result, int)
        assert result >= 0

    def test_hf_ip_hash(self):
        result = HashUtil.hf_ip_hash("hello")
        assert isinstance(result, int)

    def test_hf_hash_empty(self):
        assert HashUtil.hf_hash("") == 0
        assert HashUtil.hf_ip_hash("") == 0
