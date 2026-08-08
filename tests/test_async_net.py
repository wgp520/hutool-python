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
