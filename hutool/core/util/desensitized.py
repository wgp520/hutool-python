class DesensitizedUtil:
    """数据脱敏工具类"""

    @staticmethod
    def chinese_name(name: str) -> str:
        """中文姓名脱敏：保留姓，名替换为*

        示例：张三 -> 张*，欧阳娜娜 -> 欧***

        :param name: 中文姓名
        :return: 脱敏后的姓名
        """
        if not name:
            return ""
        name = name.strip()
        if len(name) <= 1:
            return name
        elif len(name) == 2:
            return name[0] + "*"
        else:
            return name[0] + "*" * (len(name) - 1)

    @staticmethod
    def id_card(idcard: str, before: int = 3, after: int = 4) -> str:
        """身份证脱敏

        保留前before位和后after位，中间用*替换

        :param idcard: 身份证号
        :param before: 保留前N位，默认3
        :param after: 保留后N位，默认4
        :return: 脱敏后的身份证号
        """
        if not idcard:
            return ""
        idcard = idcard.strip()
        length = len(idcard)
        if before + after >= length:
            return idcard
        return idcard[:before] + "*" * (length - before - after) + idcard[length - after :]

    @staticmethod
    def mobile_phone(phone: str) -> str:
        """手机号脱敏：138****1234

        :param phone: 手机号
        :return: 脱敏后的手机号
        """
        if not phone:
            return ""
        phone = phone.strip()
        if len(phone) < 7:
            return phone
        return phone[:3] + "****" + phone[7:]

    @staticmethod
    def fixed_phone(phone: str) -> str:
        """固定电话脱敏

        保留区号和后4位，中间用*替换

        :param phone: 固定电话
        :return: 脱敏后的固定电话
        """
        if not phone:
            return ""
        phone = phone.strip()
        # 查找分隔符位置（区号后的'-'）
        dash_pos = phone.find("-")
        if dash_pos == -1:
            # 无分隔符，按规则：前3位为区号保留，后4位保留
            if len(phone) <= 7:
                return phone[:3] + "****" if len(phone) > 3 else phone
            return phone[:3] + "*" * (len(phone) - 7) + phone[-4:]
        area_code = phone[:dash_pos]
        number = phone[dash_pos + 1 :]
        if len(number) <= 4:
            return area_code + "-" + number
        return area_code + "-" + "*" * (len(number) - 4) + number[-4:]

    @staticmethod
    def email(email: str) -> str:
        """邮箱脱敏：t***@example.com

        保留@前的首字母和@后的完整域名

        :param email: 邮箱地址
        :return: 脱敏后的邮箱
        """
        if not email:
            return ""
        email = email.strip()
        at_pos = email.find("@")
        if at_pos <= 0:
            return email
        prefix = email[:at_pos]
        domain = email[at_pos:]
        if len(prefix) <= 1:
            return prefix + "***" + domain
        return prefix[0] + "***" + domain

    @staticmethod
    def address(address: str, sensitive_size: int = 6) -> str:
        """地址脱敏

        从敏感_size位之前开始替换为*

        :param address: 地址
        :param sensitive_size: 需要脱敏的字符数，默认6
        :return: 脱敏后的地址
        """
        if not address:
            return ""
        address = address.strip()
        length = len(address)
        if sensitive_size >= length:
            return "*" * length
        return address[: length - sensitive_size] + "*" * sensitive_size

    @staticmethod
    def bank_card(card: str) -> str:
        """银行卡脱敏

        保留前4位和后4位，中间用*替换

        :param card: 银行卡号
        :return: 脱敏后的银行卡号
        """
        if not card:
            return ""
        card = card.strip().replace(" ", "")
        if len(card) <= 8:
            return card
        return card[:4] + "*" * (len(card) - 8) + card[-4:]

    @staticmethod
    def password(password: str) -> str:
        """密码脱敏：全部替换为*

        :param password: 密码
        :return: 脱敏后的密码（全为*）
        """
        if not password:
            return ""
        return "*" * len(password)

    @staticmethod
    def car_license(license_no: str) -> str:
        """车牌号脱敏

        保留前2位和后1位，中间用*替换

        :param license_no: 车牌号
        :return: 脱敏后的车牌号
        """
        if not license_no:
            return ""
        license_no = license_no.strip()
        if len(license_no) <= 3:
            return license_no
        return license_no[:2] + "*" * (len(license_no) - 3) + license_no[-1:]

    @staticmethod
    def ipv4(ipv4: str) -> str:
        """IPv4脱敏

        保留前两段，后两段替换为*

        :param ipv4: IPv4地址
        :return: 脱敏后的IPv4地址
        """
        if not ipv4:
            return ""
        ipv4 = ipv4.strip()
        parts = ipv4.split(".")
        if len(parts) != 4:
            return ipv4
        return parts[0] + "." + parts[1] + ".*.*"

    @staticmethod
    def license_plate(plate: str) -> str:
        """车牌号脱敏

        保留省份简称和地区代码，后面替换为*

        :param plate: 车牌号
        :return: 脱敏后的车牌号
        """
        if not plate:
            return ""
        plate = plate.strip()
        if len(plate) <= 2:
            return plate
        return plate[:2] + "*" * (len(plate) - 2)

    @staticmethod
    def first_mask(str_val: str, mask_char: str = "*", mask_len: int = 4) -> str:
        """对字符串前 N 个字符进行脱敏。

        :param str_val: 原始字符串
        :param mask_char: 替换字符，默认 ``"*"``
        :param mask_len: 脱敏长度，默认 4
        :return: 脱敏后的字符串
        """
        if not str_val:
            return ""
        if len(str_val) <= mask_len:
            return mask_char * len(str_val)
        return mask_char * mask_len + str_val[mask_len:]

    @staticmethod
    def ipv6(ipv6: str) -> str:
        """IPv6 地址脱敏，保留前两段，后两段替换为 ``*``。

        :param ipv6: IPv6 地址
        :return: 脱敏后的 IPv6 地址
        """
        if not ipv6:
            return ""
        parts = ipv6.split(":")
        if len(parts) <= 2:
            return ipv6
        return ":".join(parts[:2]) + ":*:*"

    @staticmethod
    def passport(passport: str) -> str:
        """护照号脱敏，保留首位和末位，中间替换为 ``*``。

        :param passport: 护照号
        :return: 脱敏后的护照号
        """
        if not passport or len(passport) <= 2:
            return passport or ""
        return passport[0] + "*" * (len(passport) - 2) + passport[-1]

    @staticmethod
    def credit_code(code: str) -> str:
        """统一社会信用代码脱敏，保留前 6 位和后 4 位。

        :param code: 统一社会信用代码
        :return: 脱敏后的代码
        """
        if not code:
            return ""
        if len(code) <= 10:
            return code
        return code[:6] + "*" * (len(code) - 10) + code[-4:]

    @staticmethod
    def clear_mask(s: str, replacement: str = "*") -> str:
        """清空字符串，全部替换为指定字符。

        :param s: 原始字符串
        :param replacement: 替换字符，默认 '*'
        :return: 替换后的字符串
        """
        if not s:
            return ""
        return replacement * len(s)

    @staticmethod
    def clear_to_null(s: str):
        """清空字符串，返回 None。

        :param s: 原始字符串
        :return: None
        """
        return None

    @staticmethod
    def desensitized(s: str, start: int, end: int, replacement: str = "*") -> str:
        """通用脱敏：将指定区间内的字符替换为指定字符。

        :param s: 原始字符串
        :param start: 开始位置（包含）
        :param end: 结束位置（不包含）
        :param replacement: 替换字符，默认 '*'
        :return: 脱敏后的字符串
        """
        if not s:
            return ""
        if start < 0:
            start = 0
        if end > len(s):
            end = len(s)
        if start >= end:
            return s
        return s[:start] + replacement * (end - start) + s[end:]

    @staticmethod
    def user_id(user_id_val) -> str:
        """用户 ID 脱敏。

        :param user_id_val: 用户 ID
        :return: 脱敏后的用户 ID
        """
        if user_id_val is None:
            return ""
        s = str(user_id_val)
        if len(s) <= 2:
            return s
        return s[0] + "*" * (len(s) - 1)
