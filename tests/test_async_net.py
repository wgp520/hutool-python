"""AsyncNetUtil 异步网络工具测试（离线，不依赖外网）。"""

import asyncio
import socket
import threading

import pytest

from hutool import AsyncNetUtil


@pytest.fixture
def echo_server():
    """启动一个本地 TCP 回显服务器，返回其监听端口。"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 0))
    sock.listen(1)
    port = sock.getsockname()[1]

    def serve():
        while True:
            try:
                conn, _ = sock.accept()
            except OSError:
                break
            try:
                data = conn.recv(4096)
                if data:
                    conn.sendall(data)
            finally:
                conn.close()

    t = threading.Thread(target=serve, daemon=True)
    t.start()
    yield port
    sock.close()


class TestAsyncNetUtil:
    async def test_is_open_true(self, echo_server):
        assert await AsyncNetUtil.is_open("127.0.0.1", echo_server) is True

    async def test_is_open_false(self):
        # 端口 1 不可能被普通进程监听，连接应被拒绝
        assert await AsyncNetUtil.is_open("127.0.0.1", 1) is False

    async def test_is_open_invalid_port(self):
        assert await AsyncNetUtil.is_open("127.0.0.1", 999999) is False

    async def test_net_cat(self, echo_server):
        result = await AsyncNetUtil.net_cat("127.0.0.1", echo_server, "ping")
        assert result == "ping"

    async def test_ping_open_connection_ok(self, monkeypatch):
        async def fake_open(host, port, **kwargs):
            return object(), object()

        monkeypatch.setattr(asyncio, "open_connection", fake_open)
        assert await AsyncNetUtil.ping("example.com") is True

    async def test_ping_refused(self, monkeypatch):
        async def fake_open(host, port, **kwargs):
            raise OSError("refused")

        monkeypatch.setattr(asyncio, "open_connection", fake_open)
        # localhost 连接失败时按约定视为可达
        assert await AsyncNetUtil.ping("localhost") is True
        assert await AsyncNetUtil.ping("1.2.3.4") is False

    async def test_get_ip_by_host(self, monkeypatch):
        monkeypatch.setattr(socket, "gethostbyname", lambda h: "9.9.9.9")
        assert await AsyncNetUtil.get_ip_by_host("example.com") == "9.9.9.9"

    async def test_get_dns_info(self, monkeypatch):
        monkeypatch.setattr(
            socket,
            "getaddrinfo",
            lambda *a, **k: [(socket.AF_INET, 1, 6, "", ("1.2.3.4", 0))],
        )
        monkeypatch.setattr(socket, "gethostbyname_ex", lambda h: (h, [], ["1.2.3.4"]))
        info = await AsyncNetUtil.get_dns_info("example.com")
        assert info["ips"] == ["1.2.3.4"]
        assert info["canonical"] == "example.com"

    async def test_get_local_ip(self, monkeypatch):
        class _FakeSock:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def connect(self, *a):
                pass

            def getsockname(self):
                return ("10.0.0.5", 12345)

        monkeypatch.setattr(socket, "socket", lambda *a, **k: _FakeSock())
        assert await AsyncNetUtil.get_local_ip() == "10.0.0.5"

    # ---- 纯计算 / 地址解析（薄壳委托同步实现） ----

    async def test_is_valid_port(self):
        assert await AsyncNetUtil.is_valid_port(80) is True
        assert await AsyncNetUtil.is_valid_port(70000) is False

    async def test_ipv4_to_long(self):
        assert await AsyncNetUtil.ipv4_to_long("1.2.3.4") == 16909060

    async def test_long_to_ipv4(self):
        assert await AsyncNetUtil.long_to_ipv4(16909060) == "1.2.3.4"

    async def test_is_inner(self):
        assert await AsyncNetUtil.is_inner("192.168.1.1") is True
        assert await AsyncNetUtil.is_inner("8.8.8.8") is False

    async def test_hide_ip_part(self):
        assert await AsyncNetUtil.hide_ip_part("1.2.3.4") == "1.2.3.*"

    async def test_to_ip_list_cidr(self):
        # /30 网络含 2 个可用主机地址（去掉网络地址与广播地址）
        assert await AsyncNetUtil.to_ip_list("192.168.1.0/30") == [
            "192.168.1.1",
            "192.168.1.2",
        ]

    async def test_get_localhost_str(self):
        assert await AsyncNetUtil.get_localhost_str() == "localhost"

    async def test_idn_to_ascii(self):
        assert await AsyncNetUtil.idn_to_ascii("例子.com") == "xn--fsqu00a.com"

    async def test_parse_cookies(self):
        assert await AsyncNetUtil.parse_cookies("a=1; b=2") == {"a": "1", "b": "2"}

    async def test_to_absolute_url(self):
        # 基于 urllib.parse.urljoin 语义：base 的最后一段被相对路径替换
        assert await AsyncNetUtil.to_absolute_url("http://x.com/a", "b/c") == "http://x.com/b/c"

    async def test_get_local_host_name(self):
        assert await AsyncNetUtil.get_local_host_name() == await AsyncNetUtil.get_localhost()

    # ---- 网络 / 系统 I/O（run_in_executor 委托，避免阻塞事件循环） ----

    async def test_get_usable_local_port(self):
        port = await AsyncNetUtil.get_usable_local_port()
        assert 1024 <= port <= 0xFFFF
        assert await AsyncNetUtil.is_usable_local_port(port) is True

    async def test_get_usable_local_ports(self):
        ports = await AsyncNetUtil.get_usable_local_ports(3)
        assert len(ports) == 3

    async def test_get_localhost(self):
        assert await AsyncNetUtil.get_localhost()

    async def test_get_host_name(self):
        assert await AsyncNetUtil.get_host_name()

    async def test_get_mac_address(self):
        mac = await AsyncNetUtil.get_mac_address()
        assert len(mac.split(":")) == 6

    async def test_local_ipv4s(self):
        ips = await AsyncNetUtil.local_ipv4s()
        assert isinstance(ips, list)
