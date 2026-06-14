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

        :param string: 输入字符串
        :return: 32位哈希值
        """
        if string is None:
            return 0
        hash_val = 0xAAAAAAAA
        for i, ch in enumerate(string):
            if (i & 1) == 0:
                hash_val ^= (hash_val << 7) ^ ord(ch) ^ (hash_val >> 3)
            else:
                hash_val ^= ~((hash_val << 11) ^ ord(ch) ^ (hash_val >> 5))
            hash_val &= 0xFFFFFFFF
        return hash_val

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
