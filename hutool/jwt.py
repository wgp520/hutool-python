"""JWT工具类"""

import base64
import json
import time
from typing import Optional

import jwt


class JWTUtil:
    """JWT工具类"""

    @staticmethod
    def create_token(payload: dict, secret: str, algorithm: str = "HS256") -> str:
        """创建JWT token

        :param payload: 载荷数据
        :param secret: 密钥
        :param algorithm: 加密算法，默认为 'HS256'
        :return: JWT token字符串
        """
        return jwt.encode(payload, secret, algorithm=algorithm)

    @staticmethod
    def parse_token(token: str, secret: str, algorithm: str = "HS256") -> dict:
        """解析并验证JWT token

        :param token: JWT token字符串
        :param secret: 密钥
        :param algorithm: 加密算法，默认为 'HS256'
        :return: 解析后的载荷数据
        :raises jwt.ExpiredSignatureError: token已过期
        :raises jwt.InvalidTokenError: token无效
        """
        return jwt.decode(token, secret, algorithms=[algorithm])

    @staticmethod
    def verify(token: str, secret: str, algorithm: str = "HS256") -> bool:
        """验证token是否有效

        :param token: JWT token字符串
        :param secret: 密钥
        :param algorithm: 加密算法，默认为 'HS256'
        :return: token是否有效
        """
        try:
            jwt.decode(token, secret, algorithms=[algorithm])
            return True
        except jwt.PyJWTError:
            return False

    @staticmethod
    def get_payload(token: str) -> dict:
        """获取token的payload（不验证签名）

        :param token: JWT token字符串
        :return: 解析后的载荷数据
        :raises jwt.DecodeError: token格式无效
        """
        return jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256", "HS384", "HS512"])

    @staticmethod
    def create_token_with_expire(
        payload: dict, secret: str, expire_seconds: int = 3600, algorithm: str = "HS256"
    ) -> str:
        """创建带过期时间的JWT token

        :param payload: 载荷数据
        :param secret: 密钥
        :param expire_seconds: 过期时间（秒），默认3600
        :param algorithm: 算法
        :return: JWT token字符串
        """
        import copy

        data = copy.deepcopy(payload)
        data["exp"] = int(time.time()) + expire_seconds
        return jwt.encode(data, secret, algorithm=algorithm)

    @staticmethod
    def parse_header(token: str) -> dict:
        """获取token的header部分（不验证签名）

        :param token: JWT token字符串
        :return: header字典
        """
        header_segment = token.split(".")[0]
        # 补齐base64 padding
        padding = 4 - len(header_segment) % 4
        if padding != 4:
            header_segment += "=" * padding
        decoded = base64.urlsafe_b64decode(header_segment)
        return json.loads(decoded)

    @staticmethod
    def is_expired(token: str) -> bool:
        """判断token是否已过期

        :param token: JWT token字符串
        :return: 是否已过期
        """
        try:
            payload = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256", "HS384", "HS512"])
            exp = payload.get("exp")
            if exp is None:
                return False
            return int(time.time()) > exp
        except jwt.PyJWTError:
            return True

    @staticmethod
    def get_claim(token: str, claim_name: str):
        """获取token中的指定声明（不验证签名）

        :param token: JWT token字符串
        :param claim_name: 声明名称
        :return: 声明值，不存在返回None
        """
        payload = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256", "HS384", "HS512"])
        return payload.get(claim_name)

    @staticmethod
    def generate_key(algorithm: str = "HS256") -> bytes:
        """生成JWT签名密钥

        :param algorithm: 算法
        :return: 随机密钥
        """
        import secrets

        key_lengths = {
            "HS256": 32,
            "HS384": 48,
            "HS512": 64,
        }
        length = key_lengths.get(algorithm, 32)
        return secrets.token_bytes(length)

    @staticmethod
    def create_token_with_claims(
        secret: str,
        algorithm: str = "HS256",
        issuer: Optional[str] = None,
        subject: Optional[str] = None,
        audience: Optional[str] = None,
        expire_seconds: int = 3600,
        **extra_claims,
    ) -> str:
        """创建包含标准声明的JWT token

        :param secret: 密钥
        :param algorithm: 算法
        :param issuer: 签发者
        :param subject: 主题
        :param audience: 受众
        :param expire_seconds: 过期时间
        :param extra_claims: 额外声明
        :return: JWT token字符串
        """
        payload = {}
        if issuer is not None:
            payload["iss"] = issuer
        if subject is not None:
            payload["sub"] = subject
        if audience is not None:
            payload["aud"] = audience
        payload["exp"] = int(time.time()) + expire_seconds
        payload["iat"] = int(time.time())
        payload.update(extra_claims)
        return jwt.encode(payload, secret, algorithm=algorithm)
