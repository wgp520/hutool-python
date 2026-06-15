"""JWT工具类"""

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
