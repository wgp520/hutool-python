import pytest

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

    def test_ipv6_to_big_integer(self):
        n = NetUtil.ipv6_to_big_integer("::1")
        assert n == 1

    def test_big_integer_to_ipv6(self):
        ip = NetUtil.big_integer_to_ipv6(1)
        assert ip == "::1"

    def test_ipv6_roundtrip(self):
        n = NetUtil.ipv6_to_big_integer("fe80::1")
        assert NetUtil.big_integer_to_ipv6(n) == "fe80::1"

    def test_ipv6_invalid(self):
        with pytest.raises(ValueError):
            NetUtil.ipv6_to_big_integer("not_an_ipv6")

    def test_get_usable_local_ports(self):
        ports = NetUtil.get_usable_local_ports(3)
        assert len(ports) == 3
        assert len(set(ports)) == 3  # all unique

    def test_hide_ip_part_from_long(self):
        result = NetUtil.hide_ip_part_from_long(NetUtil.ipv4_to_long("192.168.1.1"))
        assert result == "192.168.1.*"

    def test_local_ipv6s(self):
        result = NetUtil.local_ipv6s()
        assert isinstance(result, list)

    def test_to_ip_list_cidr(self):
        ips = NetUtil.to_ip_list("192.168.1.0/30")
        assert len(ips) == 2
        assert "192.168.1.1" in ips

    def test_to_ip_list_range(self):
        ips = NetUtil.to_ip_list("192.168.1.1-192.168.1.3")
        assert len(ips) == 3
        assert ips[0] == "192.168.1.1"
        assert ips[2] == "192.168.1.3"

    def test_to_ip_list_single(self):
        ips = NetUtil.to_ip_list("10.0.0.1")
        assert ips == ["10.0.0.1"]

    def test_local_ips(self):
        result = NetUtil.local_ips()
        assert isinstance(result, list)

    def test_get_localhost_str(self):
        assert NetUtil.get_localhost_str() == "localhost"

    def test_idn_to_ascii(self):
        result = NetUtil.idn_to_ascii("example.com")
        assert result == "example.com"

    def test_idn_to_ascii_none(self):
        assert NetUtil.idn_to_ascii(None) == ""

    def test_is_unknown(self):
        assert NetUtil.is_unknown(None) is True
        assert NetUtil.is_unknown("") is True
        assert NetUtil.is_unknown("unknown") is True
        assert NetUtil.is_unknown("UNKNOWN") is True
        assert NetUtil.is_unknown("192.168.1.1") is False

    def test_ping(self):
        # localhost should be reachable
        assert NetUtil.ping("localhost") is True
        assert NetUtil.ping(None) is False

    def test_parse_cookies(self):
        cookies = NetUtil.parse_cookies("name=value; session=abc123; token")
        assert cookies["name"] == "value"
        assert cookies["session"] == "abc123"
        assert cookies["token"] == ""

    def test_parse_cookies_empty(self):
        assert NetUtil.parse_cookies("") == {}
        assert NetUtil.parse_cookies(None) == {}

    def test_get_dns_info(self):
        info = NetUtil.get_dns_info("localhost")
        assert "hostname" in info
        assert "ips" in info

    def test_get_dns_info_empty(self):
        info = NetUtil.get_dns_info("")
        assert info["ips"] == []

    def test_get_host_name(self):
        name = NetUtil.get_host_name()
        assert isinstance(name, str)
        assert len(name) > 0

    def test_get_host_address(self):
        addr = NetUtil.get_host_address()
        assert isinstance(addr, str)
        assert len(addr) > 0
        # 应为合法 IP 格式
        assert "." in addr

    def test_get_host_name_matches_get_localhost(self):
        assert NetUtil.get_host_name() == NetUtil.get_localhost()


class TestIpv4Util:
    def test_format_ip_block(self):
        result = Ipv4Util.format_ip_block("192.168.1.1", "255.255.255.0")
        assert result == "192.168.1.0/24"

    def test_get_mask_bit_by_mask(self):
        result = Ipv4Util.get_mask_bit_by_mask("255.255.255.0")
        assert result == 24

    def test_ipv4_to_long(self):
        assert Ipv4Util.ipv4_to_long("0.0.0.0") == 0
        assert Ipv4Util.ipv4_to_long("192.168.1.1") == 3232235777
        assert Ipv4Util.ipv4_to_long("255.255.255.255") == 4294967295

    def test_long_to_ipv4(self):
        assert Ipv4Util.long_to_ipv4(0) == "0.0.0.0"
        assert Ipv4Util.long_to_ipv4(3232235777) == "192.168.1.1"
        assert Ipv4Util.long_to_ipv4(4294967295) == "255.255.255.255"

    def test_ipv4_long_roundtrip(self):
        ip = "10.0.0.1"
        assert Ipv4Util.long_to_ipv4(Ipv4Util.ipv4_to_long(ip)) == ip

    def test_ipv4_to_long_invalid(self):
        with pytest.raises(ValueError):
            Ipv4Util.ipv4_to_long("abc")

    def test_ipv4_to_long_no_octets(self):
        with pytest.raises(ValueError):
            Ipv4Util.ipv4_to_long("1.2.3")

    def test_long_to_ipv4_out_of_range(self):
        with pytest.raises(ValueError):
            Ipv4Util.long_to_ipv4(-1)
        with pytest.raises(ValueError):
            Ipv4Util.long_to_ipv4(2**32)

    def test_get_begin_ip_str(self):
        assert Ipv4Util.get_begin_ip_str("192.168.1.0/24") == "192.168.1.0"
        assert Ipv4Util.get_begin_ip_str("10.0.0.0/8") == "10.0.0.0"

    def test_get_end_ip_str(self):
        assert Ipv4Util.get_end_ip_str("192.168.1.0/24") == "192.168.1.255"
        assert Ipv4Util.get_end_ip_str("10.0.0.0/8") == "10.255.255.255"

    def test_get_begin_ip_long(self):
        assert Ipv4Util.get_begin_ip_long("192.168.1.0/24") == Ipv4Util.ipv4_to_long("192.168.1.0")

    def test_get_end_ip_long(self):
        assert Ipv4Util.get_end_ip_long("192.168.1.0/24") == Ipv4Util.ipv4_to_long("192.168.1.255")

    def test_count_by_mask_bit(self):
        assert Ipv4Util.count_by_mask_bit(24) == 256
        assert Ipv4Util.count_by_mask_bit(32) == 1
        assert Ipv4Util.count_by_mask_bit(16) == 65536

    def test_get_mask_by_mask_bit(self):
        assert Ipv4Util.get_mask_by_mask_bit(24) == "255.255.255.0"
        assert Ipv4Util.get_mask_by_mask_bit(16) == "255.255.0.0"
        assert Ipv4Util.get_mask_by_mask_bit(32) == "255.255.255.255"

    def test_is_mask_valid(self):
        assert Ipv4Util.is_mask_valid("255.255.255.0") is True
        assert Ipv4Util.is_mask_valid("255.255.0.0") is True
        assert Ipv4Util.is_mask_valid("255.255.255.255") is True
        assert Ipv4Util.is_mask_valid("255.255.255.1") is False
        assert Ipv4Util.is_mask_valid("0.0.0.0") is True

    def test_is_mask_bit_valid(self):
        assert Ipv4Util.is_mask_bit_valid(0) is True
        assert Ipv4Util.is_mask_bit_valid(24) is True
        assert Ipv4Util.is_mask_bit_valid(32) is True
        assert Ipv4Util.is_mask_bit_valid(33) is False
        assert Ipv4Util.is_mask_bit_valid(-1) is False

    def test_is_inner_ip(self):
        assert Ipv4Util.is_inner_ip("10.0.0.1") is True
        assert Ipv4Util.is_inner_ip("172.16.0.1") is True
        assert Ipv4Util.is_inner_ip("192.168.1.1") is True
        assert Ipv4Util.is_inner_ip("127.0.0.1") is True
        assert Ipv4Util.is_inner_ip("8.8.8.8") is False

    def test_matches(self):
        assert Ipv4Util.matches("192.168.1.1", "192.168.1.*") is True
        assert Ipv4Util.matches("192.168.1.1", "192.168.1.1") is True
        assert Ipv4Util.matches("192.168.1.2", "192.168.1.1") is False
        assert Ipv4Util.matches("10.0.0.1", "10.0.*.*") is True

    def test_format_ip_block_v2(self):
        result = Ipv4Util.format_ip_block("192.168.1.0", "255.255.255.0")
        assert result == "192.168.1.0/24"

    def test_list(self):
        ips = Ipv4Util.list("192.168.1.0/30")
        assert len(ips) == 2
        assert "192.168.1.1" in ips
        assert "192.168.1.2" in ips

    def test_get_mask_bit(self):
        assert Ipv4Util.get_mask_bit("255.255.255.0") == 24
        assert Ipv4Util.get_mask_bit("255.255.0.0") == 16
        assert Ipv4Util.get_mask_bit("invalid") is None


class TestMaskBit:
    def test_get_mask(self):
        result = MaskBit.get(24)
        assert result == "255.255.255.0"

    def test_get_bit(self):
        result = MaskBit.get_mask_bit("255.255.255.0")
        assert result == 24

    def test_is_inner_ip(self):
        assert NetUtil.is_inner_ip("192.168.1.1") is True
        assert NetUtil.is_inner_ip("10.0.0.1") is True
        assert NetUtil.is_inner_ip("8.8.8.8") is False

    def test_is_in_range(self):
        assert NetUtil.is_in_range("192.168.1.100", "192.168.1.0/24") is True
        assert NetUtil.is_in_range("10.0.0.1", "192.168.1.0/24") is False

    def test_hide_ip_part(self):
        assert NetUtil.hide_ip_part("192.168.1.100") == "192.168.1.*"
        assert NetUtil.hide_ip_part("") == ""

    def test_local_ipv4s(self):
        result = NetUtil.local_ipv4s()
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_get_local_host_name(self):
        result = NetUtil.get_local_host_name()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_ip_by_host(self):
        result = NetUtil.get_ip_by_host("localhost")
        assert result in ("127.0.0.1", "::1", "")

    def test_get_ip_by_host_invalid(self):
        result = NetUtil.get_ip_by_host("invalid.host.that.does.not.exist")
        assert result == ""

    def test_to_absolute_url(self):
        result = NetUtil.to_absolute_url("http://example.com/a/b", "../c")
        assert result == "http://example.com/c"
