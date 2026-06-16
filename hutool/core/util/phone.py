import re


class PhoneUtil:
    """手机号工具类"""

    # 中国大陆手机号正则
    _MOBILE_PATTERN = re.compile(r"^1[3-9]\d{9}$")

    # 香港手机号正则（8位，5/6/9开头）
    _MOBILE_HK_PATTERN = re.compile(r"^[569]\d{7}$")

    # 台湾手机号正则（09开头10位）
    _MOBILE_TW_PATTERN = re.compile(r"^09\d{8}$")

    # 澳门手机号正则（6开头8位）
    _MOBILE_MO_PATTERN = re.compile(r"^6\d{7}$")

    # 座机正则（区号-号码，区号3-4位，号码7-8位）
    _FIXED_PHONE_PATTERN = re.compile(r"^0\d{2,3}-?\d{7,8}$")

    # 座机正则（含 400/800 号码）
    _TEL_400_800_PATTERN = re.compile(r"^(400|800)\d{7}$")

    @staticmethod
    def is_mobile(phone: str) -> bool:
        """是否为中国大陆手机号

        :param phone: 手机号字符串
        :return: 是否合法
        """
        if not phone:
            return False
        return bool(PhoneUtil._MOBILE_PATTERN.match(phone.strip()))

    @staticmethod
    def is_mobile_hk(phone: str) -> bool:
        """是否为香港手机号（8位，5/6/9开头）

        :param phone: 手机号字符串
        :return: 是否合法
        """
        if not phone:
            return False
        return bool(PhoneUtil._MOBILE_HK_PATTERN.match(phone.strip()))

    @staticmethod
    def is_mobile_tw(phone: str) -> bool:
        """是否为台湾手机号（09开头10位）

        :param phone: 手机号字符串
        :return: 是否合法
        """
        if not phone:
            return False
        return bool(PhoneUtil._MOBILE_TW_PATTERN.match(phone.strip()))

    @staticmethod
    def is_mobile_mo(phone: str) -> bool:
        """是否为澳门手机号（6开头8位）

        :param phone: 手机号字符串
        :return: 是否合法
        """
        if not phone:
            return False
        return bool(PhoneUtil._MOBILE_MO_PATTERN.match(phone.strip()))

    @staticmethod
    def is_phone(phone: str) -> bool:
        """是否为电话号码（手机或座机）

        :param phone: 电话号码字符串
        :return: 是否合法
        """
        if not phone:
            return False
        phone = phone.strip()
        return PhoneUtil.is_mobile(phone) or bool(PhoneUtil._FIXED_PHONE_PATTERN.match(phone))

    @staticmethod
    def is_mobile_simple(phone: str) -> bool:
        """简单判断是否为手机号（11位数字，1开头）

        相比 :meth:`is_mobile` 规则更宽松，仅检查长度和首位。

        :param phone: 手机号字符串
        :return: 是否可能是手机号
        """
        if not phone:
            return False
        phone = phone.strip()
        return len(phone) == 11 and phone[0] == "1" and phone.isdigit()

    @staticmethod
    def hide_before(phone: str) -> str:
        """隐藏前3位，如 138****1234

        :param phone: 手机号字符串
        :return: 脱敏后的手机号
        """
        if not phone:
            return ""
        phone = phone.strip()
        if len(phone) < 7:
            return phone
        return phone[:3] + "****" + phone[7:]

    @staticmethod
    def hide_between(phone: str) -> str:
        """隐藏中间4位，如 138****1234

        :param phone: 手机号字符串
        :return: 脱敏后的手机号
        """
        if not phone:
            return ""
        phone = phone.strip()
        if len(phone) < 11:
            return phone
        return phone[:3] + "****" + phone[7:]

    @staticmethod
    def hide_after(phone: str) -> str:
        """隐藏后4位

        :param phone: 手机号字符串
        :return: 脱敏后的手机号
        """
        if not phone:
            return ""
        phone = phone.strip()
        if len(phone) < 4:
            return phone
        return phone[:-4] + "****"

    @staticmethod
    def sub_before(phone: str) -> str:
        """获取手机号前3位

        :param phone: 手机号字符串
        :return: 前3位
        """
        if not phone:
            return ""
        return phone.strip()[:3]

    @staticmethod
    def sub_after(phone: str) -> str:
        """获取手机号后4位

        :param phone: 手机号字符串
        :return: 后4位
        """
        if not phone:
            return ""
        return phone.strip()[-4:]

    @staticmethod
    def is_tel(tel: str) -> bool:
        """是否为座机号码（含区号）。

        :param tel: 座机号码
        :return: 是否合法
        """
        if not tel:
            return False
        return bool(PhoneUtil._FIXED_PHONE_PATTERN.match(tel.strip()))

    @staticmethod
    def is_tel_400_800(tel: str) -> bool:
        """是否为 400 或 800 号码。

        :param tel: 电话号码
        :return: 是否合法
        """
        if not tel:
            return False
        tel = tel.strip().replace("-", "")
        return bool(PhoneUtil._TEL_400_800_PATTERN.match(tel))

    @staticmethod
    def sub_between(phone: str, begin: int, end: int) -> str:
        """截取手机号指定位之间的内容。

        :param phone: 手机号
        :param begin: 起始索引（包含）
        :param end: 结束索引（不包含）
        :return: 截取的子串
        """
        if not phone:
            return ""
        return phone.strip()[begin:end]

    @staticmethod
    def sub_tel_before(tel: str) -> str:
        """获取座机号码的区号部分。

        :param tel: 座机号码
        :return: 区号
        """
        if not tel:
            return ""
        tel = tel.strip()
        parts = tel.split("-")
        return parts[0] if parts else ""

    @staticmethod
    def sub_tel_after(tel: str) -> str:
        """获取座机号码的号码部分（去掉区号）。

        :param tel: 座机号码
        :return: 号码部分
        """
        if not tel:
            return ""
        tel = tel.strip()
        parts = tel.split("-", 1)
        return parts[1] if len(parts) > 1 else parts[0]
