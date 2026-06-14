from hutool import Ipv4Util, MaskBit, NetUtil


class TestNetUtil:
    def test_get_local_ip(self):
        result = NetUtil.get_local_ip()
        assert isinstance(result, str)
        assert "." in result

    def test_is_inner(self):
        assert NetUtil.is_inner("127.0.0.1") is True
        assert NetUtil.is_inner("10.0.0.1") is True
        assert NetUtil.is_inner("192.168.1.1") is True
        assert NetUtil.is_inner("8.8.8.8") is False

    def test_ipv4_to_long(self):
        result = NetUtil.ipv4_to_long("192.168.1.1")
        assert isinstance(result, int)
        assert result > 0

    def test_long_to_ipv4(self):
        long_ip = NetUtil.ipv4_to_long("192.168.1.1")
        result = NetUtil.long_to_ipv4(long_ip)
        assert result == "192.168.1.1"

    def test_is_open(self):
        # Test with likely closed port
        result = NetUtil.is_open("127.0.0.1", 19999, timeout=500)
        assert isinstance(result, bool)

    def test_is_valid_port(self):
        assert NetUtil.is_valid_port(80) is True
        assert NetUtil.is_valid_port(0) is True
        assert NetUtil.is_valid_port(65536) is False

    def test_get_localhost(self):
        result = NetUtil.get_localhost()
        assert isinstance(result, str)
        assert len(result) > 0


class TestIpv4Util:
    def test_format_ip_block(self):
        result = Ipv4Util.format_ip_block("192.168.1.1", "255.255.255.0")
        assert result == "192.168.1.1/24"

    def test_get_mask_bit_by_mask(self):
        result = Ipv4Util.get_mask_bit_by_mask("255.255.255.0")
        assert result == 24


class TestMaskBit:
    def test_get_mask(self):
        result = MaskBit.get(24)
        assert result == "255.255.255.0"

    def test_get_bit(self):
        result = MaskBit.get_mask_bit("255.255.255.0")
        assert result == 24
