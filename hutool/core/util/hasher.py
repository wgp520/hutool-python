"""哈希工具类"""


class HashUtil:
    """哈希工具类，对应 Java cn.hutool.core.util.HashUtil

    提供多种非加密哈希算法的纯Python实现。
    所有算法结果通过 & 0xFFFFFFFF 限制为32位无符号整数。
    """

    @staticmethod
    def fnv1(data: bytes) -> int:
        """FNV-1 哈希算法

        :param data: 字节数组
        :return: 32位哈希值
        """
        if data is None:
            return 0
        FNV_OFFSET = 0x811C9DC5
        FNV_PRIME = 0x01000193
        hash_val = FNV_OFFSET
        for b in data:
            hash_val = (hash_val * FNV_PRIME) & 0xFFFFFFFF
            hash_val ^= b
            hash_val &= 0xFFFFFFFF
        return hash_val

    @staticmethod
    def fnv1a(data: bytes) -> int:
        """FNV-1a 哈希算法（与FNV-1的区别在于异或和乘法的顺序相反）

        :param data: 字节数组
        :return: 32位哈希值
        """
        if data is None:
            return 0
        FNV_OFFSET = 0x811C9DC5
        FNV_PRIME = 0x01000193
        hash_val = FNV_OFFSET
        for b in data:
            hash_val ^= b
            hash_val = (hash_val * FNV_PRIME) & 0xFFFFFFFF
        return hash_val

    @staticmethod
    def bkdr_hash(string: str) -> int:
        """BKDR 哈希算法

        由Brian Kernighan与Dennis Ritchie提出，种子数为131。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        seed = 131
        hash_val = 0
        for ch in string:
            hash_val = (hash_val * seed + ord(ch)) & 0xFFFFFFFF
        return hash_val

    @staticmethod
    def ap_hash(string: str) -> int:
        """AP 哈希算法

        由Arash Partow提出，具有很好的分布效果。
        初始值为 0。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 0
        for i, ch in enumerate(string):
            if (i & 1) == 0:
                hash_val ^= ((hash_val << 7) ^ ord(ch) ^ (hash_val >> 3)) & 0xFFFFFFFF
            else:
                hash_val ^= (~((hash_val << 11) ^ ord(ch) ^ (hash_val >> 5))) & 0xFFFFFFFF
        return hash_val & 0xFFFFFFFF

    @staticmethod
    def djb_hash(string: str) -> int:
        """DJB 哈希算法

        由Daniel J. Bernstein提出，使用初始值5381。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 5381
        for ch in string:
            hash_val = ((hash_val << 5) + hash_val + ord(ch)) & 0xFFFFFFFF
        return hash_val

    @staticmethod
    def js_hash(string: str) -> int:
        """JS 哈希算法

        Justin Sobel提出的哈希算法。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 0x4E67C6A7
        for ch in string:
            hash_val ^= (hash_val << 5) + ord(ch) + (hash_val >> 2)
            hash_val &= 0xFFFFFFFF
        return hash_val

    @staticmethod
    def rs_hash(string: str) -> int:
        """RS 哈希算法

        Robert Sedgwicks提出的哈希算法。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        a = 63689
        b = 378551
        hash_val = 0
        for ch in string:
            hash_val = (hash_val * a + ord(ch)) & 0xFFFFFFFF
            a = (a * b) & 0xFFFFFFFF
        return hash_val

    @staticmethod
    def sdbm_hash(string: str) -> int:
        """SDBM 哈希算法

        开源数据库SDBM使用的哈希算法。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 0
        for ch in string:
            hash_val = ord(ch) + (hash_val << 6) + (hash_val << 16) - hash_val
            hash_val &= 0xFFFFFFFF
        return hash_val

    @staticmethod
    def elf_hash(string: str) -> int:
        """ELF 哈希算法

        UNIX系统ELF文件格式中使用的哈希算法。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 0
        x = 0
        for ch in string:
            hash_val = (hash_val << 4) + ord(ch)
            x = hash_val & 0xF0000000
            if x != 0:
                hash_val ^= x >> 24
            hash_val &= ~x
            hash_val &= 0xFFFFFFFF
        return hash_val

    @staticmethod
    def dek_hash(string: str) -> int:
        """DEK 哈希算法

        由Donald E. Knuth提出。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = len(string)
        for ch in string:
            hash_val = ((hash_val << 5) ^ (hash_val >> 27) ^ ord(ch)) & 0xFFFFFFFF
        return hash_val

    @staticmethod
    def bp_hash(string: str) -> int:
        """BP 哈希算法

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 0
        for ch in string:
            hash_val = (hash_val << 7) ^ ord(ch)
            hash_val &= 0xFFFFFFFF
        return hash_val

    @staticmethod
    def pjw_hash(string: str) -> int:
        """PJW 哈希算法

        Peter J. Weinberger提出的哈希算法，常用于编译器符号表。

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 0
        for ch in string:
            hash_val = (hash_val << 4) + ord(ch)
            high_bits = hash_val & 0xF0000000
            if high_bits != 0:
                hash_val ^= high_bits >> 24
                hash_val &= ~high_bits
            hash_val &= 0xFFFFFFFF
        return hash_val

    @staticmethod
    def java_hash_code(string: str) -> int:
        """Java String.hashCode() 兼容实现

        使用 Java 的 s*31+c 算法，结果与Java完全一致。
        Java的hashCode使用有符号32位整数，此方法返回无符号表示。

        算法: h = h * 31 + char[i]

        :param string: 输入字符串
        :return: 32位哈希值（无符号表示，范围与Java有符号int一一对应）
        """
        if string is None:
            return 0
        h = 0
        for ch in string:
            h = (31 * h + ord(ch)) & 0xFFFFFFFF
        return h

    @staticmethod
    def additive_hash(key: str, prime: int) -> int:
        """累加哈希算法。

        :param key: 输入字符串
        :param prime: 质数
        :return: 哈希值
        """
        if key is None:
            return 0
        hash_val = len(key)
        for ch in key:
            hash_val += ord(ch)
        return hash_val % prime

    @staticmethod
    def rotating_hash(key: str, prime: int) -> int:
        """旋转哈希算法。

        :param key: 输入字符串
        :param prime: 质数
        :return: 哈希值
        """
        if key is None:
            return 0
        hash_val = len(key)
        for ch in key:
            hash_val = ((hash_val << 4) ^ (hash_val >> 28) ^ ord(ch)) & 0xFFFFFFFF
        return hash_val % prime

    @staticmethod
    def one_by_one_hash(key: str) -> int:
        """一次一个哈希算法。

        :param key: 输入字符串
        :return: 32位哈希值
        """
        if key is None:
            return 0
        hash_val = 0
        for ch in key:
            hash_val = (hash_val + ord(ch)) & 0xFFFFFFFF
            hash_val = (hash_val + (hash_val << 10)) & 0xFFFFFFFF
            hash_val ^= (hash_val >> 6) & 0xFFFFFFFF
        hash_val = (hash_val + (hash_val << 3)) & 0xFFFFFFFF
        hash_val ^= (hash_val >> 11) & 0xFFFFFFFF
        hash_val = (hash_val + (hash_val << 15)) & 0xFFFFFFFF
        return hash_val

    @staticmethod
    def bernstein_hash(key: str) -> int:
        """Bernstein 哈希算法。

        :param key: 输入字符串
        :return: 哈希值
        """
        if key is None:
            return 0
        hash_val = 0
        for ch in key:
            hash_val = (33 * hash_val + ord(ch)) & 0xFFFFFFFF
        return hash_val

    @staticmethod
    def universal_hash(key: str, mask: int, tab: list) -> int:
        """通用哈希算法（Universal Hashing）。

        :param key: 输入字符串
        :param mask: 掩码
        :param tab: 查找表（长度至少为 len(key) * 8）
        :return: 哈希值
        """
        if key is None:
            return 0
        hash_val = len(key)
        for i, ch in enumerate(key):
            k = ord(ch)
            for bit in range(8):
                idx = i * 8 + bit
                if idx < len(tab) and (k & (1 << bit)) == 0:
                    hash_val ^= tab[idx]
        return hash_val & mask

    @staticmethod
    def zobrist_hash(key: str, mask: int, tab: list) -> int:
        """Zobrist 哈希算法。

        :param key: 输入字符串
        :param mask: 掩码
        :param tab: 二维查找表 tab[i][ord(ch)]
        :return: 哈希值
        """
        if key is None:
            return 0
        hash_val = len(key)
        for i, ch in enumerate(key):
            if i < len(tab) and ord(ch) < len(tab[i]):
                hash_val ^= tab[i][ord(ch)]
        return hash_val & mask

    @staticmethod
    def int_hash(key: int) -> int:
        """Thomas Wang 32 位整数哈希算法。

        :param key: 整数
        :return: 32位哈希值
        """
        key = key & 0xFFFFFFFF
        key = (key + ~(key << 15)) & 0xFFFFFFFF
        key ^= key >> 10
        key = (key + (key << 3)) & 0xFFFFFFFF
        key ^= key >> 6
        key = (key + ~(key << 11)) & 0xFFFFFFFF
        key ^= key >> 16
        return key & 0xFFFFFFFF

    @staticmethod
    def tianl_hash(s: str) -> int:
        """TianL 哈希算法。

        :param s: 输入字符串
        :return: 哈希值
        """
        if not s:
            return 0
        length = len(s)
        if length <= 256:
            hash_val = 16777216 * (length - 1)
        else:
            hash_val = 4278190080

        if length <= 96:
            for i in range(1, length + 1):
                uc_char = ord(s[i - 1])
                if ord("A") <= uc_char <= ord("Z"):
                    uc_char += 32
                hash_val += (3 * i * uc_char * uc_char + 5 * i * uc_char + 7 * i + 11 * uc_char) % 16777216
        else:
            for i in range(1, 97):
                uc_char = ord(s[i + length - 97])
                if ord("A") <= uc_char <= ord("Z"):
                    uc_char += 32
                hash_val += (3 * i * uc_char * uc_char + 5 * i * uc_char + 7 * i + 11 * uc_char) % 16777216
        if hash_val < 0:
            hash_val = -hash_val
        return hash_val

    @staticmethod
    def mix_hash(s: str) -> int:
        """混合哈希算法，输出 64 位值。

        高 32 位为 Java hashCode，低 32 位为 FNV-1 哈希。

        :param s: 输入字符串
        :return: 64位哈希值
        """
        if s is None:
            return 0
        # 高32位：Java hashCode
        h = 0
        for ch in s:
            h = (31 * h + ord(ch)) & 0xFFFFFFFF
        hash_val = h << 32
        # 低32位：FNV-1
        fnv_offset = 0x811C9DC5
        fnv_prime = 0x01000193
        fnv_hash = fnv_offset
        for b in s.encode("utf-8"):
            fnv_hash = (fnv_hash * fnv_prime) & 0xFFFFFFFF
            fnv_hash ^= b
            fnv_hash &= 0xFFFFFFFF
        hash_val |= fnv_hash
        return hash_val

    # ------------------------------------------------------------------
    # MurmurHash（纯 Python 实现）
    # ------------------------------------------------------------------

    @staticmethod
    def murmur32(data: bytes, seed: int = 0) -> int:
        """MurmurHash3 32 位算法。

        :param data: 字节数组
        :param seed: 种子，默认 0
        :return: 32位哈希值
        """
        try:
            import mmh3

            return mmh3.hash(data, seed) & 0xFFFFFFFF
        except ImportError:
            return HashUtil._murmur32_impl(data, seed)

    @staticmethod
    def _murmur32_impl(data: bytes, seed: int = 0) -> int:
        """MurmurHash3 32 位纯 Python 实现。"""
        if data is None:
            return 0
        length = len(data)
        h1 = seed & 0xFFFFFFFF
        c1 = 0xCC9E2D51
        c2 = 0x1B873593

        # body
        nblocks = length // 4
        for i in range(nblocks):
            k1 = (
                (data[i * 4] & 0xFF)
                | ((data[i * 4 + 1] & 0xFF) << 8)
                | ((data[i * 4 + 2] & 0xFF) << 16)
                | ((data[i * 4 + 3] & 0xFF) << 24)
            )
            k1 = (k1 * c1) & 0xFFFFFFFF
            k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
            k1 = (k1 * c2) & 0xFFFFFFFF
            h1 ^= k1
            h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
            h1 = (h1 * 5 + 0xE6546B64) & 0xFFFFFFFF

        # tail
        tail = data[nblocks * 4 :]
        k1 = 0
        tail_len = length & 3
        if tail_len >= 3:
            k1 ^= (tail[2] & 0xFF) << 16
        if tail_len >= 2:
            k1 ^= (tail[1] & 0xFF) << 8
        if tail_len >= 1:
            k1 ^= tail[0] & 0xFF
            k1 = (k1 * c1) & 0xFFFFFFFF
            k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
            k1 = (k1 * c2) & 0xFFFFFFFF
            h1 ^= k1

        # finalization
        h1 ^= length
        h1 ^= h1 >> 16
        h1 = (h1 * 0x85EBCA6B) & 0xFFFFFFFF
        h1 ^= h1 >> 13
        h1 = (h1 * 0xC2B2AE35) & 0xFFFFFFFF
        h1 ^= h1 >> 16
        return h1 & 0xFFFFFFFF

    @staticmethod
    def murmur64(data: bytes, seed: int = 0) -> int:
        """MurmurHash 64 位算法。

        :param data: 字节数组
        :param seed: 种子，默认 0
        :return: 64位哈希值
        """
        return HashUtil._murmur64_impl(data, seed)

    @staticmethod
    def _murmur64_impl(data: bytes, seed: int = 0) -> int:
        """MurmurHash2 64 位纯 Python 实现。"""
        if data is None:
            return 0
        m = 0xC6A4A7935BD1E995
        r = 47
        length = len(data)
        h = (seed ^ (length * m)) & 0xFFFFFFFFFFFFFFFF

        nblocks = length // 8
        for i in range(nblocks):
            k = int.from_bytes(data[i * 8 : i * 8 + 8], "little")
            k = (k * m) & 0xFFFFFFFFFFFFFFFF
            k ^= k >> r
            k = (k * m) & 0xFFFFFFFFFFFFFFFF
            h ^= k
            h = (h * m) & 0xFFFFFFFFFFFFFFFF

        tail = data[nblocks * 8 :]
        tail_len = len(tail)
        if tail_len >= 7:
            h ^= (tail[6] & 0xFF) << 48
        if tail_len >= 6:
            h ^= (tail[5] & 0xFF) << 40
        if tail_len >= 5:
            h ^= (tail[4] & 0xFF) << 32
        if tail_len >= 4:
            h ^= (tail[3] & 0xFF) << 24
        if tail_len >= 3:
            h ^= (tail[2] & 0xFF) << 16
        if tail_len >= 2:
            h ^= (tail[1] & 0xFF) << 8
        if tail_len >= 1:
            h ^= tail[0] & 0xFF
            h = (h * m) & 0xFFFFFFFFFFFFFFFF

        h ^= h >> r
        h = (h * m) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> r
        return h

    @staticmethod
    def murmur128(data: bytes, seed: int = 0) -> tuple:
        """MurmurHash3 128 位算法。

        :param data: 字节数组
        :param seed: 种子，默认 0
        :return: (h1, h2) 两个 64 位哈希值
        """
        return HashUtil._murmur128_impl(data, seed)

    @staticmethod
    def _murmur128_impl(data: bytes, seed: int = 0) -> tuple:
        """MurmurHash3 128 位（x64）纯 Python 实现。"""
        if data is None:
            return (0, 0)
        length = len(data)
        h1 = seed & 0xFFFFFFFFFFFFFFFF
        h2 = seed & 0xFFFFFFFFFFFFFFFF
        c1 = 0x87C37B91114253D5
        c2 = 0x4CF5AD432745937F

        nblocks = length // 16
        for i in range(nblocks):
            block = data[i * 16 : i * 16 + 16]
            k1 = int.from_bytes(block[0:8], "little")
            k2 = int.from_bytes(block[8:16], "little")

            k1 = (k1 * c1) & 0xFFFFFFFFFFFFFFFF
            k1 = ((k1 << 31) | (k1 >> 33)) & 0xFFFFFFFFFFFFFFFF
            k1 = (k1 * c2) & 0xFFFFFFFFFFFFFFFF
            h1 ^= k1
            h1 = ((h1 << 27) | (h1 >> 37)) & 0xFFFFFFFFFFFFFFFF
            h1 = (h1 + h2 + 5) & 0xFFFFFFFFFFFFFFFF

            k2 = (k2 * c2) & 0xFFFFFFFFFFFFFFFF
            k2 = ((k2 << 33) | (k2 >> 31)) & 0xFFFFFFFFFFFFFFFF
            k2 = (k2 * c1) & 0xFFFFFFFFFFFFFFFF
            h2 ^= k2
            h2 = ((h2 << 31) | (h2 >> 33)) & 0xFFFFFFFFFFFFFFFF
            h2 = (h1 + h2 + 5) & 0xFFFFFFFFFFFFFFFF

        # tail
        tail = data[nblocks * 16 :]
        k1 = 0
        k2 = 0
        tail_len = len(tail)
        if tail_len >= 15:
            k2 ^= (tail[14] & 0xFF) << 48
        if tail_len >= 14:
            k2 ^= (tail[13] & 0xFF) << 40
        if tail_len >= 13:
            k2 ^= (tail[12] & 0xFF) << 32
        if tail_len >= 12:
            k2 ^= (tail[11] & 0xFF) << 24
        if tail_len >= 11:
            k2 ^= (tail[10] & 0xFF) << 16
        if tail_len >= 10:
            k2 ^= (tail[9] & 0xFF) << 8
        if tail_len >= 9:
            k2 ^= tail[8] & 0xFF
            k2 = (k2 * c2) & 0xFFFFFFFFFFFFFFFF
            k2 = ((k2 << 33) | (k2 >> 31)) & 0xFFFFFFFFFFFFFFFF
            k2 = (k2 * c1) & 0xFFFFFFFFFFFFFFFF
            h2 ^= k2
        if tail_len >= 8:
            k1 ^= (tail[7] & 0xFF) << 56
        if tail_len >= 7:
            k1 ^= (tail[6] & 0xFF) << 48
        if tail_len >= 6:
            k1 ^= (tail[5] & 0xFF) << 40
        if tail_len >= 5:
            k1 ^= (tail[4] & 0xFF) << 32
        if tail_len >= 4:
            k1 ^= (tail[3] & 0xFF) << 24
        if tail_len >= 3:
            k1 ^= (tail[2] & 0xFF) << 16
        if tail_len >= 2:
            k1 ^= (tail[1] & 0xFF) << 8
        if tail_len >= 1:
            k1 ^= tail[0] & 0xFF
            k1 = (k1 * c1) & 0xFFFFFFFFFFFFFFFF
            k1 = ((k1 << 31) | (k1 >> 33)) & 0xFFFFFFFFFFFFFFFF
            k1 = (k1 * c2) & 0xFFFFFFFFFFFFFFFF
            h1 ^= k1

        # finalization
        h1 ^= length
        h2 ^= length
        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 + h1) & 0xFFFFFFFFFFFFFFFF
        h1 = HashUtil._fmix64(h1)
        h2 = HashUtil._fmix64(h2)
        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 + h1) & 0xFFFFFFFFFFFFFFFF
        return (h1, h2)

    @staticmethod
    def _fmix64(k: int) -> int:
        """64 位 finalization mix。"""
        k ^= k >> 33
        k = (k * 0xFF51AFD7ED558CCD) & 0xFFFFFFFFFFFFFFFF
        k ^= k >> 33
        k = (k * 0xC4CEB9FE1A85EC53) & 0xFFFFFFFFFFFFFFFF
        k ^= k >> 33
        return k

    # ------------------------------------------------------------------
    # CityHash（简化实现）
    # ------------------------------------------------------------------

    @staticmethod
    def city_hash32(data: bytes) -> int:
        """CityHash 32 位算法（简化实现）。

        :param data: 字节数组
        :return: 32位哈希值
        """
        if data is None:
            return 0
        length = len(data)
        h = 0
        for b in data:
            h = (h * 31 + (b & 0xFF)) & 0xFFFFFFFF
        h ^= length
        h = ((h ^ (h >> 16)) * 0x85EBCA6B) & 0xFFFFFFFF
        h = ((h ^ (h >> 13)) * 0xC2B2AE35) & 0xFFFFFFFF
        h ^= h >> 16
        return h

    @staticmethod
    def city_hash64(data: bytes, seed: int = 0) -> int:
        """CityHash 64 位算法（简化实现）。

        :param data: 字节数组
        :param seed: 种子，默认 0
        :return: 64位哈希值
        """
        if data is None:
            return 0
        h = seed & 0xFFFFFFFFFFFFFFFF
        for b in data:
            h = (h * 31 + (b & 0xFF)) & 0xFFFFFFFFFFFFFFFF
        length = len(data)
        h ^= length
        h ^= h >> 33
        h = (h * 0xFF51AFD7ED558CCD) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 33
        h = (h * 0xC4CEB9FE1A85EC53) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 33
        return h

    @staticmethod
    def city_hash128(data: bytes) -> tuple:
        """CityHash 128 位算法（简化实现）。

        :param data: 字节数组
        :return: (h1, h2) 两个 64 位哈希值
        """
        if data is None:
            return (0, 0)
        h1 = HashUtil.city_hash64(data, 0)
        h2 = HashUtil.city_hash64(data, 0x9AE16A3B2F90404F)
        return (h1, h2)

    # ------------------------------------------------------------------
    # MetroHash（简化实现）
    # ------------------------------------------------------------------

    @staticmethod
    def metro_hash64(data: bytes, seed: int = 0) -> int:
        """MetroHash 64 位算法（简化实现）。

        :param data: 字节数组
        :param seed: 种子，默认 0
        :return: 64位哈希值
        """
        if data is None:
            return 0
        h = (seed + 0x6C62272E07BB0142) & 0xFFFFFFFFFFFFFFFF
        for b in data:
            h = (h + (b & 0xFF) + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
            h ^= h >> 29
            h = (h * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
            h ^= h >> 32
        return h

    @staticmethod
    def metro_hash128(data: bytes, seed: int = 0) -> tuple:
        """MetroHash 128 位算法（简化实现）。

        :param data: 字节数组
        :param seed: 种子，默认 0
        :return: (h1, h2) 两个 64 位哈希值
        """
        if data is None:
            return (0, 0)
        h1 = HashUtil.metro_hash64(data, seed)
        h2 = HashUtil.metro_hash64(data, seed + 1)
        return (h1, h2)

    # ------------------------------------------------------------------
    # HF Hash
    # ------------------------------------------------------------------

    @staticmethod
    def hf_hash(data: str) -> int:
        """HF 哈希算法。

        :param data: 输入字符串
        :return: 哈希值
        """
        if not data:
            return 0
        hash_val = 0
        for i, ch in enumerate(data):
            hash_val += ord(ch) * 3 * i
        if hash_val < 0:
            hash_val = -hash_val
        return hash_val

    @staticmethod
    def hf_ip_hash(data: str) -> int:
        """HF IP 哈希算法。

        :param data: 输入字符串
        :return: 哈希值
        """
        if not data:
            return 0
        hash_val = 0
        length = len(data)
        for i in range(length):
            hash_val += ord(data[i % 4]) ^ ord(data[i])
        return hash_val
