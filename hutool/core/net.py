"""网络工具类，提供端口检测、IP地址处理、子网掩码转换等功能"""

import ipaddress
import random
import socket
import uuid
from socket import AF_INET, SO_REUSEADDR, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET
from typing import Final, Optional

__all__ = ("Ipv4Util", "MaskBit", "NetUtil")


class MaskBit:
    """掩码位和掩码之间的对应关系"""

    MASK_BIT_MAP: Final[dict] = {
        1: "128.0.0.0",
        2: "192.0.0.0",
        3: "224.0.0.0",
        4: "240.0.0.0",
        5: "248.0.0.0",
        6: "252.0.0.0",
        7: "254.0.0.0",
        8: "255.0.0.0",
        9: "255.128.0.0",
        10: "255.192.0.0",
        11: "255.224.0.0",
        12: "255.240.0.0",
        13: "255.248.0.0",
        14: "255.252.0.0",
        15: "255.254.0.0",
        16: "255.255.0.0",
        17: "255.255.128.0",
        18: "255.255.192.0",
        19: "255.255.224.0",
        20: "255.255.240.0",
        21: "255.255.248.0",
        22: "255.255.252.0",
        23: "255.255.254.0",
        24: "255.255.255.0",
        25: "255.255.255.128",
        26: "255.255.255.192",
        27: "255.255.255.224",
        28: "255.255.255.240",
        29: "255.255.255.248",
        30: "255.255.255.252",
        31: "255.255.255.254",
        32: "255.255.255.255",
    }

    # 反向映射：掩码字符串 -> 掩码位
    _MASK_TO_BIT: Final[dict] = {v: k for k, v in MASK_BIT_MAP.items()}

    @staticmethod
    def get(mask_bit: int) -> str:
        """
        根据掩码位获取掩码

        :param mask_bit: 掩码位，范围1-32
        :return: 掩码字符串，如"255.255.255.0"
        :raises KeyError: 掩码位不在合法范围内
        """
        return MaskBit.MASK_BIT_MAP[mask_bit]

    @staticmethod
    def get_mask_bit(mask: str) -> Optional[int]:
        """
        根据掩码获取掩码位

        :param mask: 掩码的点分十进制表示，如"255.255.255.0"
        :return: 掩码位，如24；如果掩码不合法则返回None
        """
        return MaskBit._MASK_TO_BIT.get(mask)


class Ipv4Util:
    """IPV4地址工具类"""

    LOCAL_IP: Final[str] = "127.0.0.1"
    # IP段的分割符
    IP_SPLIT_MARK: Final[str] = "-"
    # IP与掩码的分割符
    IP_MASK_SPLIT_MARK: Final[str] = "/"
    # 最大掩码位
    IP_MASK_MAX: Final[int] = 32

    @staticmethod
    def format_ip_block(ip: str, mask: str) -> str:
        """
        格式化IP段

        :param ip: IP地址
        :param mask: 掩码
        :return: 返回xxx.xxx.xxx.xxx/mask的格式
        """
        return ip + Ipv4Util.IP_MASK_SPLIT_MARK + str(Ipv4Util.get_mask_bit_by_mask(mask))

    @staticmethod
    def get_mask_bit_by_mask(mask: str) -> int:
        """
        根据子网掩码转换为掩码位

        :param mask: 掩码的点分十进制表示，例如"255.255.255.0"
        :return: 掩码位，例如24
        :raises ValueError: 子网掩码非法
        """
        mask_bit = MaskBit.get_mask_bit(mask)
        if mask_bit is None:
            raise ValueError("Invalid netmask: " + mask)
        return mask_bit


class NetUtil:
    """网络工具类，提供端口检测、IP获取、地址转换等功能"""

    # 本地IPv4地址
    LOCAL_IP: Final[str] = Ipv4Util.LOCAL_IP
    # 默认最小端口，1024
    PORT_RANGE_MIN: Final[int] = 1024
    # 默认最大端口，65535
    PORT_RANGE_MAX: Final[int] = 0xFFFF

    @staticmethod
    def is_usable_local_port(port: int) -> bool:
        """
        检测本地端口可用性

        :param port: 被检测的端口
        :return: 是否可用
        """
        if not NetUtil.is_valid_port(port):
            return False

        # 使用TCP协议检测
        try:
            with socket.socket(AF_INET, SOCK_STREAM) as s:
                s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                s.bind((NetUtil.LOCAL_IP, port))
        except OSError:
            return False

        # 使用UDP协议检测
        try:
            with socket.socket(AF_INET, SOCK_DGRAM) as s:
                s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                s.bind((NetUtil.LOCAL_IP, port))
        except OSError:
            return False

        return True

    @staticmethod
    def is_valid_port(port: int) -> bool:
        """
        是否为有效的端口，此方法并不检查端口是否被占用

        :param port: 端口号
        :return: 是否有效
        """
        return 0 <= port <= NetUtil.PORT_RANGE_MAX

    @staticmethod
    def get_usable_local_port(min_port: int = PORT_RANGE_MIN, max_port: int = PORT_RANGE_MAX) -> int:
        """
        查找指定范围内的可用端口

        此方法只检测给定范围内的随机一个端口，最多检测max_port-min_port次。

        :param min_port: 端口最小值（包含）
        :param max_port: 端口最大值（包含）
        :return: 可用的端口
        :raises RuntimeError: 在指定范围内未找到可用端口
        """
        max_port_exclude = max_port + 1
        for _ in range(min_port, max_port_exclude):
            random_port = random.randint(min_port, max_port)
            if NetUtil.is_usable_local_port(random_port):
                return random_port
        raise RuntimeError(
            f"Could not find an available port in the range [{min_port}, {max_port}] "
            f"after {max_port - min_port} attempts"
        )

    @staticmethod
    def get_local_ip() -> str:
        """
        获取本机IP地址，通过UDP连接外部地址获取本机对外IP

        :return: 本机IP地址，获取失败时返回127.0.0.1
        """
        try:
            with socket.socket(AF_INET, SOCK_DGRAM) as s:
                # 不实际发送数据，仅用于获取本机出口IP
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return NetUtil.LOCAL_IP

    @staticmethod
    def get_localhost() -> str:
        """
        获取本机主机名

        :return: 主机名
        """
        return socket.gethostname()

    @staticmethod
    def get_mac_address() -> str:
        """
        获取本机MAC地址

        :return: MAC地址字符串，格式为xx:xx:xx:xx:xx:xx
        """
        mac = uuid.getnode()
        return ":".join(f"{(mac >> (8 * i)) & 0xFF:02x}" for i in reversed(range(6)))

    @staticmethod
    def is_inner(ip: str) -> bool:
        """
        判断是否为内网IP地址

        内网IP范围：
        - 10.0.0.0 ~ 10.255.255.255（A类私有地址）
        - 172.16.0.0 ~ 172.31.255.255（B类私有地址）
        - 192.168.0.0 ~ 192.168.255.255（C类私有地址）
        - 127.0.0.0 ~ 127.255.255.255（本地回环地址）

        :param ip: IP地址字符串
        :return: 是否为内网IP
        """
        if ip is None:
            return False
        try:
            addr = ipaddress.ip_address(ip)
            return addr.is_private
        except ValueError:
            return False

    @staticmethod
    def ipv4_to_long(ip: str) -> int:
        """
        将IPv4地址转换为long整型数值

        :param ip: IPv4地址字符串，如"192.168.1.1"
        :return: 对应的long整型值
        :raises ValueError: IP地址格式非法
        """
        try:
            return int(ipaddress.IPv4Address(ip))
        except ipaddress.AddressValueError as e:
            raise ValueError(f"非法的IPv4地址: {ip}") from e

    @staticmethod
    def long_to_ipv4(long_ip: int) -> str:
        """
        将long整型数值转换为IPv4地址

        :param long_ip: long整型值
        :return: IPv4地址字符串
        :raises ValueError: 数值不在合法范围内
        """
        if long_ip < 0 or long_ip > 0xFFFFFFFF:
            raise ValueError(f"非法的long型IP值: {long_ip}")
        return str(ipaddress.IPv4Address(long_ip))

    @staticmethod
    def is_open(host: str, port: int, timeout: int = 2000) -> bool:
        """
        检测远程主机端口是否可连接

        :param host: 主机地址
        :param port: 端口号
        :param timeout: 超时时间，单位毫秒，默认2000ms
        :return: 端口是否可连接
        """
        if host is None:
            return False
        if not NetUtil.is_valid_port(port):
            return False

        try:
            with socket.socket(AF_INET, SOCK_STREAM) as s:
                s.settimeout(timeout / 1000.0)
                s.connect((host, port))
            return True
        except (socket.timeout, OSError):
            return False

    @staticmethod
    def is_inner_ip(ip: str) -> bool:
        """判断是否为内网 IP（与 is_inner 相同）。

        :param ip: IP 地址字符串
        :return: 是否为内网 IP
        """
        return NetUtil.is_inner(ip)

    @staticmethod
    def is_in_range(ip: str, cidr: str) -> bool:
        """判断 IP 是否在 CIDR 范围内。

        :param ip: IP 地址字符串
        :param cidr: CIDR 格式字符串，如 "192.168.1.0/24"
        :return: 是否在范围内
        """
        try:
            return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            return False

    @staticmethod
    def hide_ip_part(ip: str) -> str:
        """遮蔽 IP 地址，将最后一段替换为 ``*``。

        :param ip: IP 地址
        :return: 遮蔽后的 IP，如 "192.168.1.*"
        """
        if not ip:
            return ip
        parts = ip.split(".")
        if len(parts) == 4:
            parts[-1] = "*"
            return ".".join(parts)
        return ip

    @staticmethod
    def local_ipv4s() -> list:
        """获取本机所有 IPv4 地址列表。

        :return: IPv4 地址列表
        """
        ips = []
        try:
            for info in socket.getaddrinfo(socket.gethostname(), None, AF_INET):
                ip = info[4][0]
                if ip not in ips:
                    ips.append(ip)
        except socket.gaierror:
            pass
        if NetUtil.LOCAL_IP not in ips:
            ips.insert(0, NetUtil.LOCAL_IP)
        return ips

    @staticmethod
    def get_local_host_name() -> str:
        """获取本机主机名（与 get_localhost 相同）。

        :return: 主机名
        """
        return NetUtil.get_localhost()

    @staticmethod
    def get_ip_by_host(hostname: str) -> str:
        """解析主机名获取 IP 地址。

        :param hostname: 主机名
        :return: IP 地址，解析失败返回空字符串
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return ""

    @staticmethod
    def to_absolute_url(base: str, relative: str) -> str:
        """将相对 URL 补全为绝对 URL。

        :param base: 基础 URL
        :param relative: 相对 URL
        :return: 绝对 URL
        """
        from urllib.parse import urljoin

        return urljoin(base, relative)
