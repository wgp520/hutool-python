"""网络工具类，提供端口检测、IP地址处理、子网掩码转换等功能"""

import ipaddress
import random
import socket
import uuid
from socket import AF_INET, AF_INET6, SO_REUSEADDR, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET
from typing import Final, List, Optional

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
    def ipv4_to_long(ip: str) -> int:
        """IPv4 地址转 long 值。

        :param ip: IPv4 地址，如 ``"192.168.1.1"``
        :return: long 值
        :raises ValueError: IP 地址格式非法
        """
        parts = ip.strip().split(".")
        if len(parts) != 4:
            raise ValueError("无效的 IPv4 地址: " + ip)
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

    @staticmethod
    def long_to_ipv4(long_ip: int) -> str:
        """long 值转 IPv4 地址。

        :param long_ip: long 值
        :return: IPv4 地址字符串
        :raises ValueError: 数值不在合法范围内
        """
        if long_ip < 0 or long_ip > 0xFFFFFFFF:
            raise ValueError(f"非法的 long 型 IP 值: {long_ip}")
        long_ip = long_ip & 0xFFFFFFFF
        return ".".join(
            [
                str((long_ip >> 24) & 0xFF),
                str((long_ip >> 16) & 0xFF),
                str((long_ip >> 8) & 0xFF),
                str(long_ip & 0xFF),
            ]
        )

    @staticmethod
    def get_begin_ip_str(cidr: str) -> str:
        """获取 CIDR 表示的网段起始 IP 地址。

        :param cidr: CIDR 格式，如 ``"192.168.1.0/24"``
        :return: 起始 IP 地址字符串
        """
        ip_str, mask_bit = cidr.strip().split("/")
        mask_bit = int(mask_bit)
        ip_long = Ipv4Util.ipv4_to_long(ip_str)
        mask = Ipv4Util._mask_bit_to_long(mask_bit)
        begin_ip = ip_long & mask
        return Ipv4Util.long_to_ipv4(begin_ip)

    @staticmethod
    def get_begin_ip_long(cidr: str) -> int:
        """获取 CIDR 表示的网段起始 IP 的 long 值。

        :param cidr: CIDR 格式
        :return: 起始 IP 的 long 值
        """
        return Ipv4Util.ipv4_to_long(Ipv4Util.get_begin_ip_str(cidr))

    @staticmethod
    def get_end_ip_str(cidr: str) -> str:
        """获取 CIDR 表示的网段结束 IP 地址。

        :param cidr: CIDR 格式，如 ``"192.168.1.0/24"``
        :return: 结束 IP 地址字符串
        """
        ip_str, mask_bit = cidr.strip().split("/")
        mask_bit = int(mask_bit)
        ip_long = Ipv4Util.ipv4_to_long(ip_str)
        mask = Ipv4Util._mask_bit_to_long(mask_bit)
        end_ip = (ip_long & mask) | (~mask & 0xFFFFFFFF)
        return Ipv4Util.long_to_ipv4(end_ip)

    @staticmethod
    def get_end_ip_long(cidr: str) -> int:
        """获取 CIDR 表示的网段结束 IP 的 long 值。

        :param cidr: CIDR 格式
        :return: 结束 IP 的 long 值
        """
        return Ipv4Util.ipv4_to_long(Ipv4Util.get_end_ip_str(cidr))

    @staticmethod
    def count_by_mask_bit(mask_bit: int) -> int:
        """根据掩码位数计算 IP 数量。

        :param mask_bit: 掩码位数（0-32）
        :return: IP 数量
        """
        if mask_bit < 0 or mask_bit > 32:
            raise ValueError("掩码位数必须在 0-32 之间")
        return 1 << (32 - mask_bit)

    @staticmethod
    def get_mask_by_mask_bit(mask_bit: int) -> str:
        """根据掩码位数获取子网掩码。

        :param mask_bit: 掩码位数（0-32）
        :return: 子网掩码字符串
        """
        if mask_bit < 0 or mask_bit > 32:
            raise ValueError("掩码位数必须在 0-32 之间")
        mask = Ipv4Util._mask_bit_to_long(mask_bit)
        return Ipv4Util.long_to_ipv4(mask)

    @staticmethod
    def get_mask_by_ip_range(begin_ip: str, end_ip: str) -> str:
        """根据 IP 范围获取子网掩码。

        :param begin_ip: 起始 IP
        :param end_ip: 结束 IP
        :return: 子网掩码字符串
        """
        begin_long = Ipv4Util.ipv4_to_long(begin_ip)
        end_long = Ipv4Util.ipv4_to_long(end_ip)
        diff = begin_long ^ end_long
        mask_bit = 32
        while diff > 0:
            diff >>= 1
            mask_bit -= 1
        return Ipv4Util.get_mask_by_mask_bit(mask_bit)

    @staticmethod
    def count_by_ip_range(begin_ip: str, end_ip: str) -> int:
        """计算两个 IP 之间的 IP 数量。

        :param begin_ip: 起始 IP
        :param end_ip: 结束 IP
        :return: IP 数量
        """
        begin_long = Ipv4Util.ipv4_to_long(begin_ip)
        end_long = Ipv4Util.ipv4_to_long(end_ip)
        return abs(end_long - begin_long) + 1

    @staticmethod
    def is_mask_valid(mask: str) -> bool:
        """检查子网掩码是否有效。

        有效掩码的二进制表示为连续的 1 后跟连续的 0。

        :param mask: 子网掩码字符串
        :return: 是否有效
        """
        try:
            mask_long = Ipv4Util.ipv4_to_long(mask)
        except (ValueError, IndexError):
            return False
        inverted = (~mask_long) & 0xFFFFFFFF
        if inverted == 0:
            return True
        return (inverted + 1) & inverted == 0

    @staticmethod
    def is_mask_bit_valid(mask_bit: int) -> bool:
        """检查掩码位数是否有效。

        :param mask_bit: 掩码位数
        :return: 是否有效（0-32）
        """
        return 0 <= mask_bit <= 32

    @staticmethod
    def is_inner_ip(ip: str) -> bool:
        """判断是否为内网 IP。

        内网 IP 范围：
        - 10.0.0.0/8
        - 172.16.0.0/12
        - 192.168.0.0/16
        - 127.0.0.0/8（本地回环）

        :param ip: IPv4 地址
        :return: 是否为内网 IP
        """
        try:
            ip_long = Ipv4Util.ipv4_to_long(ip)
        except (ValueError, IndexError):
            return False
        if (ip_long >> 24) == 10:
            return True
        if (ip_long >> 24) == 127:
            return True
        if (ip_long >> 20) == 0xAC1:
            return True
        return (ip_long >> 16) == 0xC0A8

    @staticmethod
    def matches(ip: str, pattern: str) -> bool:
        """通配符 IP 匹配。

        支持 ``*`` 通配符，如 ``"192.168.1.*"``。

        :param ip: IPv4 地址
        :param pattern: 通配符模式
        :return: 是否匹配
        """
        ip_parts = ip.strip().split(".")
        pattern_parts = pattern.strip().split(".")
        if len(ip_parts) != 4 or len(pattern_parts) != 4:
            return False
        for ip_part, pat_part in zip(ip_parts, pattern_parts):
            if pat_part == "*":
                continue
            if ip_part != pat_part:
                return False
        return True

    @staticmethod
    def list(ip_range: str) -> list:
        """列出 CIDR 网段中的所有 IP 地址（不含网络和广播地址）。

        :param ip_range: CIDR 格式，如 ``"192.168.1.0/30"``
        :return: IP 地址列表
        """
        begin = Ipv4Util.get_begin_ip_long(ip_range)
        end = Ipv4Util.get_end_ip_long(ip_range)
        if end - begin > 65536:
            raise ValueError("IP 范围过大，最多支持 65536 个地址")
        # 排除网络地址和广播地址
        if end - begin > 1:
            return [Ipv4Util.long_to_ipv4(ip) for ip in range(begin + 1, end)]
        return [Ipv4Util.long_to_ipv4(ip) for ip in range(begin, end + 1)]

    @staticmethod
    def format_ip_block(ip: str, mask: str) -> str:
        """格式化IP段

        :param ip: IP地址
        :param mask: 掩码
        :return: 返回xxx.xxx.xxx.xxx/mask的格式
        """
        mask_bit = Ipv4Util.get_mask_bit(mask)
        begin = Ipv4Util.get_begin_ip_str(ip + "/" + str(mask_bit))
        return begin + "/" + str(mask_bit)

    @staticmethod
    def get_mask_bit_by_mask(mask: str) -> int:
        """根据子网掩码转换为掩码位

        :param mask: 掩码的点分十进制表示，例如"255.255.255.0"
        :return: 掩码位，例如24
        :raises ValueError: 子网掩码非法
        """
        mask_bit = MaskBit.get_mask_bit(mask)
        if mask_bit is None:
            raise ValueError("Invalid netmask: " + mask)
        return mask_bit

    @staticmethod
    def get_mask_bit(mask: str) -> Optional[int]:
        """获取子网掩码的位数。

        :param mask: 子网掩码字符串
        :return: 掩码位数，无效掩码返回 None
        """
        try:
            mask_long = Ipv4Util.ipv4_to_long(mask)
        except (ValueError, IndexError):
            return None
        mask_bit = 0
        while mask_long & 0x80000000:
            mask_bit += 1
            mask_long = (mask_long << 1) & 0xFFFFFFFF
        return mask_bit

    @staticmethod
    def _mask_bit_to_long(mask_bit: int) -> int:
        """掩码位数转 long 值。"""
        if mask_bit == 0:
            return 0
        return (0xFFFFFFFF << (32 - mask_bit)) & 0xFFFFFFFF


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

    @staticmethod
    def ipv6_to_big_integer(ipv6: str) -> int:
        """将 IPv6 地址转为大整数。

        :param ipv6: IPv6 地址字符串
        :return: 对应的大整数
        :raises ValueError: IPv6 地址格式非法
        """
        try:
            return int(ipaddress.IPv6Address(ipv6))
        except ipaddress.AddressValueError as e:
            raise ValueError(f"非法的 IPv6 地址: {ipv6}") from e

    @staticmethod
    def big_integer_to_ipv6(n: int) -> str:
        """将大整数转为 IPv6 地址。

        :param n: 大整数
        :return: IPv6 地址字符串
        :raises ValueError: 数值不在合法范围内
        """
        if n < 0 or n > 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:
            raise ValueError(f"非法的 long 型 IPv6 值: {n}")
        return str(ipaddress.IPv6Address(n))

    @staticmethod
    def get_usable_local_ports(
        count: int,
        min_port: int = 1024,
        max_port: int = 0xFFFF,
    ) -> List[int]:
        """批量获取可用的本地端口。

        :param count: 需要的端口数量
        :param min_port: 最小端口
        :param max_port: 最大端口
        :return: 可用端口列表
        :raises RuntimeError: 无法获取足够数量的可用端口
        """
        ports = []
        attempts = 0
        max_attempts = count * 10
        while len(ports) < count and attempts < max_attempts:
            port = random.randint(min_port, max_port)
            if port not in ports and NetUtil.is_usable_local_port(port):
                ports.append(port)
            attempts += 1
        if len(ports) < count:
            raise RuntimeError(f"无法获取 {count} 个可用端口，仅获取到 {len(ports)} 个")
        return ports

    @staticmethod
    def hide_ip_part_from_long(long_ip: int) -> str:
        """从 long 型 IP 遐藏最后一段。

        :param long_ip: long 型 IP 值
        :return: 遮蔽后的 IP 字符串
        """
        try:
            ip_str = NetUtil.long_to_ipv4(long_ip)
            return NetUtil.hide_ip_part(ip_str)
        except ValueError:
            return str(long_ip)

    @staticmethod
    def local_ipv6s() -> List[str]:
        """获取本机所有 IPv6 地址列表。

        :return: IPv6 地址列表
        """
        ips = []
        try:
            for info in socket.getaddrinfo(socket.gethostname(), None, AF_INET6):
                ip = info[4][0]
                if ip not in ips:
                    ips.append(ip)
        except socket.gaierror:
            pass
        return ips

    @staticmethod
    def to_ip_list(ip_range: str) -> List[str]:
        """将 IP 范围字符串转为 IP 列表。

        支持 CIDR 格式（如 ``192.168.1.0/30``）和短横线范围
        （如 ``192.168.1.1-192.168.1.5``）。

        :param ip_range: IP 范围字符串
        :return: IP 地址列表
        """
        ip_range = ip_range.strip()
        if "/" in ip_range:
            try:
                network = ipaddress.ip_network(ip_range, strict=False)
                return [str(ip) for ip in network.hosts()]
            except ValueError:
                return []
        elif "-" in ip_range:
            parts = ip_range.split("-", 1)
            try:
                start = int(ipaddress.IPv4Address(parts[0].strip()))
                end = int(ipaddress.IPv4Address(parts[1].strip()))
                if start > end:
                    start, end = end, start
                count = end - start + 1
                if count > 65536:
                    return []
                return [str(ipaddress.IPv4Address(ip)) for ip in range(start, end + 1)]
            except (ValueError, ipaddress.AddressValueError):
                return []
        else:
            return [ip_range]

    @staticmethod
    def local_ips() -> List[str]:
        """获取所有本地 IP 地址（IPv4 + IPv6）。

        :return: IP 地址列表
        """
        ips = []
        try:
            for info in socket.getaddrinfo(socket.gethostname(), None):
                ip = info[4][0]
                if ip not in ips:
                    ips.append(ip)
        except socket.gaierror:
            pass
        return ips

    @staticmethod
    def get_localhost_str() -> str:
        """获取 localhost 字符串表示。

        :return: "localhost" 字符串
        """
        return "localhost"

    @staticmethod
    def idn_to_ascii(domain: str) -> str:
        """将国际化域名 (IDN) 转为 ASCII 形式。

        :param domain: 域名
        :return: ASCII 编码的域名
        """
        if domain is None:
            return ""
        try:
            return domain.encode("idna").decode("ascii")
        except (UnicodeError, UnicodeDecodeError):
            return domain

    @staticmethod
    def is_unknown(ip: str) -> bool:
        """判断是否为未知 IP 地址。

        未知 IP 包括 None、空字符串和 "unknown"（不区分大小写）。

        :param ip: IP 地址
        :return: 是否为未知 IP
        """
        if ip is None:
            return True
        ip = ip.strip()
        return ip == "" or ip.lower() == "unknown"

    @staticmethod
    def ping(host: str, timeout: int = 3000) -> bool:
        """Ping 测试主机是否可达。

        通过尝试建立 TCP 连接到端口 80 来检测。

        :param host: 主机地址
        :param timeout: 超时时间，单位毫秒
        :return: 是否可达
        """
        if host is None:
            return False
        try:
            with socket.socket(AF_INET, SOCK_STREAM) as s:
                s.settimeout(timeout / 1000.0)
                s.connect((host, 80))
            return True
        except (socket.timeout, OSError):
            return host in ("localhost", "127.0.0.1", "::1")

    @staticmethod
    def parse_cookies(cookie_str: str) -> dict:
        """解析 Cookie 字符串为字典。

        :param cookie_str: Cookie 字符串，如 ``"name=value; name2=value2"``
        :return: Cookie 字典
        """
        result = {}
        if not cookie_str:
            return result
        for pair in cookie_str.split(";"):
            pair = pair.strip()
            if "=" in pair:
                key, value = pair.split("=", 1)
                result[key.strip()] = value.strip()
            elif pair:
                result[pair] = ""
        return result

    @staticmethod
    def get_dns_info(hostname: str) -> dict:
        """获取主机名的 DNS 信息。

        :param hostname: 主机名
        :return: DNS 信息字典，包含 ip、aliases、family 等
        """
        result = {"hostname": hostname, "ips": [], "aliases": [], "canonical": ""}
        if not hostname:
            return result
        try:
            infos = socket.getaddrinfo(hostname, None)
            ips = []
            for info in infos:
                ip = info[4][0]
                if ip not in ips:
                    ips.append(ip)
            result["ips"] = ips
        except socket.gaierror:
            pass
        try:
            canonical, aliases, _ = socket.gethostbyname_ex(hostname)
            result["canonical"] = canonical
            result["aliases"] = aliases
        except socket.gaierror:
            pass
        return result

    @staticmethod
    def net_cat(host: str, port: int, data: str, timeout: int = 5000) -> str:
        """网络连接发送数据并接收响应（类似 nc/netcat）。

        :param host: 主机地址
        :param port: 端口号
        :param data: 要发送的数据
        :param timeout: 超时时间，单位毫秒
        :return: 接收到的响应数据
        :raises ConnectionRefusedError: 连接被拒绝
        :raises socket.timeout: 连接超时
        """
        with socket.socket(AF_INET, SOCK_STREAM) as s:
            s.settimeout(timeout / 1000.0)
            s.connect((host, port))
            s.sendall(data.encode("utf-8"))
            s.shutdown(socket.SHUT_WR)
            chunks = []
            while True:
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
                except socket.timeout:
                    break
            return b"".join(chunks).decode("utf-8", errors="replace")
