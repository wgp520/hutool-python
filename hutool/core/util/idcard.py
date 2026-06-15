import re
from datetime import date


class IdcardUtil:
    """身份证工具类"""

    # 省份代码
    _PROVINCE_CODES = {
        "11": "北京",
        "12": "天津",
        "13": "河北",
        "14": "山西",
        "15": "内蒙古",
        "21": "辽宁",
        "22": "吉林",
        "23": "黑龙江",
        "31": "上海",
        "32": "江苏",
        "33": "浙江",
        "34": "安徽",
        "35": "福建",
        "36": "江西",
        "37": "山东",
        "41": "河南",
        "42": "湖北",
        "43": "湖南",
        "44": "广东",
        "45": "广西",
        "46": "海南",
        "50": "重庆",
        "51": "四川",
        "52": "贵州",
        "53": "云南",
        "54": "西藏",
        "61": "陕西",
        "62": "甘肃",
        "63": "青海",
        "64": "宁夏",
        "65": "新疆",
        "71": "台湾",
        "81": "香港",
        "82": "澳门",
        "91": "国外",
    }

    # 加权因子（前17位）
    _WEIGHT_FACTORS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

    # 校验码对应值（余数 -> 校验码）
    _CHECK_CODES = "10X98765432"

    # 18位身份证正则
    _ID_CARD_18_PATTERN = re.compile(r"^\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$")

    # 15位身份证正则
    _ID_CARD_15_PATTERN = re.compile(r"^\d{15}$")

    @staticmethod
    def is_valid_idcard(idcard: str) -> bool:
        """校验身份证号是否有效（支持15位和18位）

        :param idcard: 身份证号
        :return: 是否有效
        """
        if not idcard:
            return False
        idcard = idcard.strip()
        if len(idcard) == 18:
            return IdcardUtil.is_valid_card18(idcard)
        elif len(idcard) == 15:
            return IdcardUtil.is_valid_card15(idcard)
        return False

    @staticmethod
    def is_valid_card18(idcard: str) -> bool:
        """校验18位身份证

        校验规则：
        1. 格式校验（17位数字 + 第18位数字或X/x）
        2. 省份代码校验
        3. 出生日期校验（合法的YYYYMMDD）
        4. 校验码计算验证（加权求和 mod 11）

        :param idcard: 18位身份证号
        :return: 是否有效
        """
        if not idcard:
            return False
        idcard = idcard.strip().upper()

        # 1. 格式校验
        if not IdcardUtil._ID_CARD_18_PATTERN.match(idcard):
            # 也接受大写X
            if not re.match(r"^\d{17}[\dX]$", idcard):
                return False

        # 2. 省份代码校验
        province = idcard[:2]
        if province not in IdcardUtil._PROVINCE_CODES:
            return False

        # 3. 出生日期校验
        birth_str = idcard[6:14]
        try:
            year = int(birth_str[:4])
            month = int(birth_str[4:6])
            day = int(birth_str[6:8])
            birth_date = date(year, month, day)
            # 日期不能在未来
            if birth_date > date.today():
                return False
        except ValueError:
            return False

        # 4. 校验码计算验证
        # 前17位数字乘以加权因子求和
        total = 0
        for i in range(17):
            total += int(idcard[i]) * IdcardUtil._WEIGHT_FACTORS[i]
        # 取模11得到校验码索引
        check_index = total % 11
        expected_check = IdcardUtil._CHECK_CODES[check_index]
        return idcard[17] == expected_check

    @staticmethod
    def is_valid_card15(idcard: str) -> bool:
        """校验15位身份证

        :param idcard: 15位身份证号
        :return: 是否有效
        """
        if not idcard:
            return False
        idcard = idcard.strip()

        # 格式校验
        if not IdcardUtil._ID_CARD_15_PATTERN.match(idcard):
            return False

        # 省份代码校验
        province = idcard[:2]
        if province not in IdcardUtil._PROVINCE_CODES:
            return False

        # 出生日期校验（15位：6位地区码 + 6位出生日期YYMMDD + 3位顺序码）
        try:
            year = int(idcard[6:8])
            # 15位身份证的年份默认为19xx
            year += 1900
            month = int(idcard[8:10])
            day = int(idcard[10:12])
            birth_date = date(year, month, day)
            if birth_date > date.today():
                return False
        except ValueError:
            return False

        return True

    @staticmethod
    def get_birth(idcard: str) -> str:
        """获取出生日期字符串，如 "19900101"

        :param idcard: 身份证号
        :return: 出生日期字符串（YYYYMMDD格式），无效则返回空字符串
        """
        if not idcard:
            return ""
        idcard = idcard.strip()
        if len(idcard) == 18:
            return idcard[6:14]
        elif len(idcard) == 15:
            return "19" + idcard[6:12]
        return ""

    @staticmethod
    def get_age(idcard: str) -> int:
        """根据身份证号获取年龄

        :param idcard: 身份证号
        :return: 年龄，无效则返回-1
        """
        if not idcard:
            return -1
        idcard = idcard.strip()
        birth_str = IdcardUtil.get_birth(idcard)
        if not birth_str or len(birth_str) != 8:
            return -1
        try:
            year = int(birth_str[:4])
            month = int(birth_str[4:6])
            day = int(birth_str[6:8])
            birth_date = date(year, month, day)
            return IdcardUtil.get_age_by_birth(birth_date)
        except ValueError:
            return -1

    @staticmethod
    def get_age_by_birth(birth_date: date) -> int:
        """根据出生日期获取年龄

        :param birth_date: 出生日期
        :return: 年龄
        """
        today = date.today()
        age = today.year - birth_date.year
        # 如果今年的生日还没到，年龄减1
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    @staticmethod
    def get_gender(idcard: str) -> str:
        """获取性别

        身份证第17位（18位身份证）或第15位（15位身份证）：
        奇数为男性，偶数为女性

        :param idcard: 身份证号
        :return: "M"（男）或 "F"（女），无效则返回空字符串
        """
        if not idcard:
            return ""
        idcard = idcard.strip()
        if len(idcard) == 18:
            gender_digit = int(idcard[16])
        elif len(idcard) == 15:
            gender_digit = int(idcard[14])
        else:
            return ""
        return "M" if gender_digit % 2 == 1 else "F"

    @staticmethod
    def get_province(idcard: str) -> str:
        """获取省份

        :param idcard: 身份证号
        :return: 省份名称，无效则返回空字符串
        """
        if not idcard:
            return ""
        idcard = idcard.strip()
        if len(idcard) < 2:
            return ""
        province_code = idcard[:2]
        return IdcardUtil._PROVINCE_CODES.get(province_code, "")

    @staticmethod
    def convert15to18(idcard15: str) -> str:
        """15位身份证转18位

        转换规则：
        1. 在第6位后插入"19"（年份补全）
        2. 计算第18位校验码

        :param idcard15: 15位身份证号
        :return: 18位身份证号，无效输入返回空字符串
        """
        if not idcard15:
            return ""
        idcard15 = idcard15.strip()
        if len(idcard15) != 15:
            return ""
        if not IdcardUtil._ID_CARD_15_PATTERN.match(idcard15):
            return ""

        # 在第6位后插入"19"
        idcard17 = idcard15[:6] + "19" + idcard15[6:]

        # 计算校验码
        total = 0
        for i in range(17):
            total += int(idcard17[i]) * IdcardUtil._WEIGHT_FACTORS[i]
        check_index = total % 11
        check_code = IdcardUtil._CHECK_CODES[check_index]

        return idcard17 + check_code

    @staticmethod
    def hide(idcard: str) -> str:
        """隐藏身份证号中间部分

        18位身份证：保留前6位和后4位，中间用****代替
        15位身份证：保留前4位和后4位，中间用****代替

        :param idcard: 身份证号
        :return: 脱敏后的身份证号
        """
        if not idcard:
            return ""
        idcard = idcard.strip()
        if len(idcard) == 18:
            return idcard[:6] + "********" + idcard[14:]
        elif len(idcard) == 15:
            return idcard[:4] + "*******" + idcard[11:]
        elif len(idcard) > 8:
            half = (len(idcard) - 4) // 2
            return idcard[:half] + "****" + idcard[half + 4 :]
        return idcard
