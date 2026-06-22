import secrets
import threading
import time
import uuid
from typing import Optional


class _SnowflakeWorkerPool:
    """模块级雪花算法工作池，跨调用维持状态"""

    _workers: dict = {}
    _lock = threading.Lock()

    @classmethod
    def get(cls, worker_id: int, datacenter_id: int) -> "_SnowflakeIdWorker":
        """
        获取或创建指定 worker_id + datacenter_id 的雪花算法工作器（线程安全）。

        :param worker_id: 工作机器ID
        :param datacenter_id: 数据中心ID
        :return: 对应的雪花算法ID生成器实例
        """
        key = (worker_id, datacenter_id)
        with cls._lock:
            if key not in cls._workers:
                cls._workers[key] = _SnowflakeIdWorker(worker_id, datacenter_id)
            return cls._workers[key]


class IdUtil:
    """ID生成工具类，对应 Java cn.hutool.core.util.IdUtil"""

    _snowflake_worker = None

    @staticmethod
    def random_uuid() -> str:
        """
        生成随机UUID（带横线格式）。

        :return: UUID字符串，如 ``"550e8400-e29b-41d4-a716-446655440000"``
        """
        return str(uuid.uuid4())

    @staticmethod
    def simple_uuid() -> str:
        """
        生成简单UUID（不带横线格式）。

        :return: 32位十六进制UUID字符串，如 ``"550e8400e29b41d4a716446655440000"``
        """
        return str(uuid.uuid4()).replace("-", "")

    @staticmethod
    def fast_uuid() -> str:
        """
        快速生成UUID（带横线格式）。

        :return: UUID字符串
        """
        return str(uuid.uuid4())

    @staticmethod
    def fast_simple_uuid() -> str:
        """
        快速生成简单UUID（不带横线格式）。

        :return: 32位十六进制UUID字符串
        """
        return str(uuid.uuid4()).replace("-", "")

    @staticmethod
    def nano_id(size: int = 21) -> str:
        """生成NanoID（URL安全的短ID）

        使用 secrets 模块实现，类似 nanoid 算法。

        :param size: 生成的ID长度，默认为21
        :return: NanoID字符串
        """
        if size <= 0:
            raise ValueError(f"size({size}) 必须为正数")
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
        return "".join(secrets.choice(alphabet) for _ in range(size))

    @staticmethod
    def snowflake_id(worker_id: int = 1, datacenter_id: int = 1) -> int:
        """生成雪花算法ID

        :param worker_id: 工作机器ID
        :param datacenter_id: 数据中心ID
        :return: 雪花算法生成的ID
        """
        return _SnowflakeWorkerPool.get(worker_id, datacenter_id).next_id()

    @staticmethod
    def unique_machine_id() -> int:
        """
        生成机器唯一 ID（64 位整数）。

        基于当前时间戳（毫秒）、进程 ID 和原子计数器组合生成，
        在同一进程内保证唯一性。

        :return: 64 位整数 ID
        """
        import os
        import threading

        # 使用模块级计数器，线程安全
        if not hasattr(IdUtil, "_machine_counter"):
            IdUtil._machine_counter = 0
            IdUtil._machine_lock = threading.Lock()

        with IdUtil._machine_lock:
            IdUtil._machine_counter = (IdUtil._machine_counter + 1) & 0xFFFF
            counter = IdUtil._machine_counter

        timestamp = int(time.time() * 1000) & 0x1FFFFFFFFFF  # 41 bits
        pid = os.getpid() & 0xFFFF  # 16 bits
        return (timestamp << 23) | (pid << 7) | (counter & 0x7F)

    @staticmethod
    def guid128(salt=None):
        # type: (Optional[str]) -> str
        """
        生成 26 字符的全局唯一 ID。

        使用 Base32 编码（Crockford 方案：0-9A-HJKMNP-TV-Z），
        由时间戳 + 随机字节 + 可选盐值哈希组成，保证全局唯一。

        :param salt: 可选盐值字符串，相同盐值会增加差异性
        :return: 26 字符的全局唯一 ID 字符串
        """
        import hashlib

        # Crockford Base32 字典（去除易混淆字符 I/L/O/U）
        _BASE32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

        # 时间戳部分（8 字节）
        ts = int(time.time() * 1000)
        ts_bytes = ts.to_bytes(8, byteorder="big")

        # 随机部分（8 字节）
        rand_bytes = secrets.token_bytes(8)

        # 如果有盐值，将其混入随机部分
        if salt is not None:
            salt_hash = hashlib.md5(salt.encode("utf-8")).digest()
            rand_bytes = bytes(a ^ b for a, b in zip(rand_bytes, salt_hash))

        # 合并为 16 字节
        raw = ts_bytes + rand_bytes

        # 转为整数再做 Base32 编码（128 位 -> 26 字符）
        num = int.from_bytes(raw, byteorder="big")
        chars = []
        for _ in range(26):
            chars.append(_BASE32[num & 0x1F])
            num >>= 5

        return "".join(reversed(chars))

    @staticmethod
    def object_id() -> str:
        """
        生成MongoDB ObjectId格式的24位十六进制字符串。

        由 4字节时间戳 + 5字节随机值 + 3字节递增计数器 组成。

        :return: 24位十六进制字符串
        """
        # 4字节时间戳 + 5字节随机值 + 3字节递增计数器
        timestamp_part = format(int(time.time()), "08x")
        random_part = secrets.token_hex(5)
        counter_part = secrets.token_hex(3)
        return timestamp_part + random_part + counter_part

    @staticmethod
    def create_snowflake(worker_id: int = 1, datacenter_id: int = 1):
        """创建雪花算法 ID 生成器。

        :param worker_id: 工作机器 ID（0-31）
        :param datacenter_id: 数据中心 ID（0-31）
        :return: _SnowflakeIdWorker 实例
        """
        return _SnowflakeIdWorker(worker_id, datacenter_id)

    @staticmethod
    def get_snowflake(worker_id: int = 1, datacenter_id: int = 1):
        """获取全局雪花算法 ID 生成器（单例）。

        :param worker_id: 工作机器 ID（0-31）
        :param datacenter_id: 数据中心 ID（0-31）
        :return: _SnowflakeIdWorker 实例
        """
        if IdUtil._snowflake_worker is None:
            IdUtil._snowflake_worker = _SnowflakeIdWorker(worker_id, datacenter_id)
        return IdUtil._snowflake_worker

    @staticmethod
    def get_snowflake_next_id(worker_id: int = 1, datacenter_id: int = 1) -> int:
        """获取下一个雪花 ID（int）。

        :param worker_id: 工作机器 ID
        :param datacenter_id: 数据中心 ID
        :return: 64 位整数 ID
        """
        return IdUtil.get_snowflake(worker_id, datacenter_id).next_id()

    @staticmethod
    def get_snowflake_next_id_str(worker_id: int = 1, datacenter_id: int = 1) -> str:
        """获取下一个雪花 ID（字符串）。

        :param worker_id: 工作机器 ID
        :param datacenter_id: 数据中心 ID
        :return: 字符串 ID
        """
        return str(IdUtil.get_snowflake_next_id(worker_id, datacenter_id))

    @staticmethod
    def unique_machine32() -> int:
        """生成 32 位机器唯一 ID。

        基于 PID + 时间戳 + 计数器组合，在同一进程内唯一。

        :return: 32 位整数 ID
        """
        return _machine_id_gen.generate32()

    @staticmethod
    def unique_machine64() -> int:
        """生成 64 位机器唯一 ID。

        基于 PID + 主机名哈希 + 时间戳 + 计数器组合，跨机器唯一。

        :return: 64 位整数 ID
        """
        return _machine_id_gen.generate64()

    @staticmethod
    def luid(separator: str = "-") -> str:
        """基于主机名的全局唯一 ID。

        格式: ``HHHHHHHH-PIDPPPP-TTTTTTTT-CCCC``

        :param separator: 分隔符，默认 ``"-"``
        :return: 全局唯一 ID 字符串
        """
        import hashlib
        import os
        import socket

        hostname = socket.gethostname()
        host_hash = hashlib.md5(hostname.encode()).hexdigest()[:8].upper()
        pid = format(os.getpid() & 0xFFFF, "04X")
        ts = format(int(time.time()) & 0xFFFFFFFF, "08X")
        counter = format(_machine_id_gen._counter & 0xFFFF, "04X")
        return separator.join([host_hash, f"PID{pid}", ts, counter])

    @staticmethod
    def is_snowflake_id(
        snowflake_id: int,
        worker_id: Optional[int] = None,
        datacenter_id: Optional[int] = None,
        check_timestamp: bool = True,
    ) -> bool:
        """判断一个数字是否为有效的雪花算法 ID，并可选验证 worker_id 和 datacenter_id 是否匹配。

        验证逻辑：

        1. 必须是正整数且不超过 63 位
        2. 解析出的时间戳必须在合理范围内（EPOCH ~ 当前时间 + 1 天）
        3. 若指定 ``worker_id``，则要求 ID 中的 worker_id 与之相等
        4. 若指定 ``datacenter_id``，则要求 ID 中的 datacenter_id 与之相等

        :param snowflake_id: 待判断的数字
        :param worker_id: 期望的工作机器 ID（0-31），为 None 时不校验
        :param datacenter_id: 期望的数据中心 ID（0-31），为 None 时不校验
        :param check_timestamp: 是否校验时间戳合理性，默认 True
        :return: 是否为有效的雪花 ID 且 worker/datacenter 匹配
        """
        if not isinstance(snowflake_id, int) or snowflake_id <= 0:
            return False

        bits = snowflake_id.bit_length()
        if bits > 63:
            return False

        # 解析各段
        wid = (snowflake_id >> _SnowflakeIdWorker.WORKER_ID_SHIFT) & _SnowflakeIdWorker.MAX_WORKER_ID
        dc_id = (snowflake_id >> _SnowflakeIdWorker.DATACENTER_ID_SHIFT) & _SnowflakeIdWorker.MAX_DATACENTER_ID
        ts = (snowflake_id >> _SnowflakeIdWorker.TIMESTAMP_LEFT_SHIFT) + _SnowflakeIdWorker.EPOCH

        # 校验 worker_id
        if worker_id is not None and wid != worker_id:
            return False

        # 校验 datacenter_id
        if datacenter_id is not None and dc_id != datacenter_id:
            return False

        # 校验时间戳范围
        if check_timestamp:
            now_ms = int(time.time() * 1000)
            # 允许未来 1 天的时钟偏差
            if ts < _SnowflakeIdWorker.EPOCH or ts > now_ms + 86400000:
                return False

        return True


class _SnowflakeIdWorker:
    """雪花算法ID生成器内部实现"""

    # 起始时间戳 (2020-01-01 00:00:00)
    EPOCH = 1577808000000

    # 各部分位数
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12

    # 最大值
    MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1  # 31
    MAX_DATACENTER_ID = (1 << DATACENTER_ID_BITS) - 1  # 31

    # 序列掩码
    SEQUENCE_MASK = (1 << SEQUENCE_BITS) - 1  # 4095

    # 左移位数
    WORKER_ID_SHIFT = SEQUENCE_BITS  # 12
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS  # 17
    TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS  # 22

    def __init__(self, worker_id: int, datacenter_id: int):
        """初始化雪花算法ID生成器

        :param worker_id: 工作机器ID，范围 [0, 31]
        :param datacenter_id: 数据中心ID，范围 [0, 31]
        """
        if worker_id < 0 or worker_id > self.MAX_WORKER_ID:
            raise ValueError(f"worker_id({worker_id}) 必须在 [0, {self.MAX_WORKER_ID}] 范围内")
        if datacenter_id < 0 or datacenter_id > self.MAX_DATACENTER_ID:
            raise ValueError(f"datacenter_id({datacenter_id}) 必须在 [0, {self.MAX_DATACENTER_ID}] 范围内")
        self._worker_id = worker_id
        self._datacenter_id = datacenter_id
        self._sequence = 0
        self._last_timestamp = -1
        self._lock = threading.Lock()

    def next_id(self) -> int:
        """
        生成下一个雪花算法ID（线程安全）。

        :return: 唯一的64位整数ID
        :raises RuntimeError: 发生时钟回拨时
        """
        with self._lock:
            timestamp = self._current_millis()
            if timestamp < self._last_timestamp:
                raise RuntimeError(f"时钟回拨，拒绝生成ID，回拨毫秒数: {self._last_timestamp - timestamp}")
            if timestamp == self._last_timestamp:
                self._sequence = (self._sequence + 1) & self.SEQUENCE_MASK
                if self._sequence == 0:
                    timestamp = self._wait_next_millis()
            else:
                self._sequence = 0
            self._last_timestamp = timestamp
            return (
                ((timestamp - self.EPOCH) << self.TIMESTAMP_LEFT_SHIFT)
                | (self._datacenter_id << self.DATACENTER_ID_SHIFT)
                | (self._worker_id << self.WORKER_ID_SHIFT)
                | self._sequence
            )

    def _current_millis(self) -> int:
        """获取当前时间戳（毫秒）"""
        return int(time.time() * 1000)

    def _wait_next_millis(self) -> int:
        """自旋等待直到下一毫秒"""
        ts = self._current_millis()
        while ts <= self._last_timestamp:
            ts = self._current_millis()
        return ts


class MachineIdGenerator:
    """机器唯一 ID 生成器（32/64 位）。

    基于 PID、主机名哈希、时间戳和计数器组合生成唯一 ID。
    """

    def __init__(self):
        import hashlib
        import os
        import socket
        import threading

        hostname = socket.gethostname()
        self._host_hash = int(hashlib.md5(hostname.encode()).hexdigest()[:8], 16)
        self._pid = os.getpid() & 0xFFFF
        self._counter = 0
        self._lock = threading.Lock()

    def generate32(self) -> int:
        """生成 32 位机器唯一 ID。

        布局: 时间戳（毫秒，12位）+ PID（8位）+ 计数器（12位）

        :return: 32 位整数
        """
        with self._lock:
            self._counter = (self._counter + 1) & 0xFFF  # 12 bits
            ts = int(time.time() * 1000) & 0xFFF  # 毫秒级，12 bits
            return ((ts << 20) | ((self._pid & 0xFF) << 12) | self._counter) & 0xFFFFFFFF

    def generate64(self) -> int:
        """生成 64 位机器唯一 ID。

        :return: 64 位整数
        """
        with self._lock:
            self._counter = (self._counter + 1) & 0xFFFF
            ts = int(time.time() * 1000) & 0x1FFFFFFFFFF
            return (ts << 23) | (self._host_hash & 0xFF) << 15 | (self._pid & 0xFF) << 7 | (self._counter & 0x7F)


# 模块级单例
_machine_id_gen = MachineIdGenerator()
