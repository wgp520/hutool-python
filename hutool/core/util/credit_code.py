class CreditCodeUtil:
    """统一社会信用代码工具类

    统一社会信用代码共18位，由以下部分组成：
    - 登记管理部门代码（1位）
    - 机构类别代码（1位）
    - 登记管理机关行政区划码（6位）
    - 主体标识码（9位）
    - 校验码（1位）
    """

    # 字符到数值的映射
    _CHAR_MAP = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    # 加权因子（前17位）
    _WEIGHT_FACTORS = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]

    # 登记管理部门代码
    _DEPT_CODES = {
        "1": "机构编制",
        "2": "外交",
        "3": "司法行政",
        "4": "文化",
        "5": "民政",
        "6": "旅游",
        "7": "宗教",
        "8": "工会",
        "9": "工商",
        "A": "机构编制",
        "B": "外交",
        "C": "机构编制",
        "D": "商务",
        "E": "其他",
    }
    # 机构类别代码对应的管理部门
    _TYPE_CODES = {
        "1": {"1": "机关", "2": "事业单位", "3": "编办直接管理机构编制的群众团体", "9": "其他"},
        "2": {"1": "外国常驻新闻机构", "9": "其他"},
        "3": {
            "1": "律师执业机构",
            "2": "公证处",
            "3": "基层法律服务所",
            "4": "司法鉴定机构",
            "5": "仲裁委员会",
            "9": "其他",
        },
        "4": {"1": "外国在华文化中心", "9": "其他"},
        "5": {"1": "社会团体", "2": "民办非企业单位", "3": "基金会", "9": "其他"},
        "6": {"1": "外国旅游部门常驻代表机构", "2": "港澳台地区旅游部门常驻代表机构", "9": "其他"},
        "7": {"1": "宗教活动场所", "2": "宗教院校", "9": "其他"},
        "8": {"1": "基层工会", "9": "其他"},
        "9": {"1": "企业", "2": "个体工商户", "3": "农民专业合作社"},
        "A": {"1": "中央编办直接管理机构编制的群众团体", "9": "其他"},
        "B": {"1": "外国常驻新闻机构", "9": "其他"},
        "C": {"1": "律师事务所", "9": "其他"},
        "D": {"1": "外国在华文化中心", "9": "其他"},
        "E": {"1": "民政", "9": "其他"},
    }

    @staticmethod
    def is_valid_credit_code(code: str) -> bool:
        """校验统一社会信用代码是否有效

        校验规则：
        1. 长度必须为18位
        2. 字符必须在允许的字符集内
        3. 登记管理部门代码和机构类别代码必须合法
        4. 校验码必须正确（使用ISO 7064:1983.MOD 37-2算法）

        :param code: 待校验的统一社会信用代码
        :return: 是否有效
        """
        if not code or len(code) != 18:
            return False

        code = code.upper()

        # 检查字符是否在允许的字符集中
        for ch in code:
            if ch not in CreditCodeUtil._CHAR_MAP:
                return False

        # 检查登记管理部门代码
        dept_code = code[0]
        if dept_code not in CreditCodeUtil._DEPT_CODES:
            return False

        # 检查机构类别代码
        type_code = code[1]
        if dept_code not in CreditCodeUtil._TYPE_CODES:
            return False
        if type_code not in CreditCodeUtil._TYPE_CODES[dept_code]:
            return False

        # 校验第18位校验码
        # 使用ISO 7064:1983.MOD 37-2算法
        check_sum = 0
        for i in range(17):
            char_index = CreditCodeUtil._CHAR_MAP.index(code[i])
            check_sum += char_index * CreditCodeUtil._WEIGHT_FACTORS[i]

        remainder = check_sum % 31
        if remainder == 0:
            remainder = 31

        expected_index = 31 - remainder
        expected_char = CreditCodeUtil._CHAR_MAP[expected_index]

        return code[17] == expected_char

    @staticmethod
    def is_credit_code_simple(code: str) -> bool:
        """简单校验统一社会信用代码（仅检查长度和字符集）。

        :param code: 待校验的代码
        :return: 是否符合基本格式
        """
        if not code or len(code) != 18:
            return False
        code = code.upper()
        for ch in code:
            if ch not in CreditCodeUtil._CHAR_MAP:
                return False
        return True

    @staticmethod
    def random_credit_code() -> str:
        """生成一个随机的统一社会信用代码（不一定能通过完整校验）。

        :return: 18 位统一社会信用代码字符串
        """
        import secrets

        chars = CreditCodeUtil._CHAR_MAP
        dept_chars = list(CreditCodeUtil._DEPT_CODES.keys())
        dept = secrets.choice(dept_chars)
        type_chars = list(CreditCodeUtil._TYPE_CODES.get(dept, {"1": ""}).keys())
        type_code = secrets.choice(type_chars) if type_chars else "1"
        # 6位行政区划码
        region = "".join(secrets.choice("0123456789") for _ in range(6))
        # 9位主体标识码
        body = "".join(secrets.choice(chars) for _ in range(9))
        # 计算校验码
        partial = dept + type_code + region + body
        check_sum = 0
        for i in range(17):
            char_index = chars.index(partial[i])
            check_sum += char_index * CreditCodeUtil._WEIGHT_FACTORS[i]
        remainder = check_sum % 31
        if remainder == 0:
            remainder = 31
        check_char = chars[31 - remainder]
        return partial + check_char
