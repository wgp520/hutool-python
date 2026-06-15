from typing import Dict

from .digest import DigestUtil


class SignUtil:
    """签名工具类

    提供常用的参数签名算法，适用于接口签名、防篡改等场景。
    签名流程：
    1. 将参数按 key 的字典序排序
    2. 拼接为 key1=value1&key2=value2&secret=xxx 格式
    3. 使用指定算法计算摘要
    """

    # 支持的算法映射
    _ALGORITHM_MAP = {
        "md5": (DigestUtil.md5_hex, False),
        "sha1": (DigestUtil.sha1_hex, False),
        "sha256": (DigestUtil.sha256_hex, False),
        "hmac_md5": (DigestUtil.hmac_md5_hex, True),
        "hmac_sha1": (DigestUtil.hmac_sha1_hex, True),
        "hmac_sha256": (DigestUtil.hmac_sha256_hex, True),
    }

    @staticmethod
    def sign_params(params: Dict[str, str], secret: str, algorithm: str = "md5") -> str:
        """对参数进行签名

        签名步骤：
        1. 将参数按 key 字典序升序排序
        2. 拼接为 key1=value1&key2=value2&secret=xxx 形式
        3. 用指定算法计算摘要并返回十六进制字符串

        :param params: 待签名的参数字典
        :param secret: 密钥
        :param algorithm: 签名算法，支持 md5 / sha1 / sha256 / hmac_md5 / hmac_sha1 / hmac_sha256
        :return: 签名后的十六进制字符串
        :raises ValueError: 不支持的算法时抛出
        """
        algo_lower = algorithm.lower()
        if algo_lower not in SignUtil._ALGORITHM_MAP:
            raise ValueError(f"不支持的签名算法: {algorithm}，支持: {', '.join(SignUtil._ALGORITHM_MAP.keys())}")

        # 1. 按 key 排序，过滤掉值为 None 的参数
        sorted_keys = sorted(params.keys())

        # 2. 拼接
        parts = []
        for key in sorted_keys:
            value = params[key]
            if value is not None:
                parts.append(f"{key}={value}")
        parts.append(f"secret={secret}")
        sign_str = "&".join(parts)

        # 3. 计算摘要
        func, is_hmac = SignUtil._ALGORITHM_MAP[algo_lower]
        if is_hmac:
            return func(sign_str, secret)
        return func(sign_str)

    @staticmethod
    def sort_sign(params: Dict[str, str], secret: str, algorithm: str = "md5") -> str:
        """排序签名（功能同 sign_params）

        这是 sign_params 的别名，方便不同调用场景使用。

        :param params: 待签名的参数字典
        :param secret: 密钥
        :param algorithm: 签名算法
        :return: 签名后的十六进制字符串
        """
        return SignUtil.sign_params(params, secret, algorithm)
