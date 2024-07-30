import random
from faker.providers import BaseProvider


class IDCardProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        # 省份地址码
        self.province_codes = {
            "河南省": "410000",
            "湖北省": "420000",
            "广东省": "440000",
            "广西壮族自治区": "450000",
            "海南省": "460000"
        }

    def id_card_number(self, province_name):
        if province_name not in self.province_codes:
            raise ValueError(f"Invalid province name: {province_name}")

        # 获取省份的地址码
        address_code = self.province_codes[province_name]

        # 随机生成城市和区县代码
        city_code = str(random.randint(0, 99)).zfill(2)
        county_code = str(random.randint(0, 99)).zfill(2)

        # 随机生成出生日期
        birth_year = str(random.randint(1950, 2002))
        birth_month = str(random.randint(1, 12)).zfill(2)
        birth_day = str(random.randint(1, 28)).zfill(2)

        # 随机生成序列号
        sequence = str(random.randint(0, 9999)).zfill(4)

        # 计算校验码
        id_number = f"{address_code}{city_code}{county_code}{birth_year}{birth_month}{birth_day}{sequence}"
        check_digit = self.calculate_check_digit(id_number)

        return f"{id_number}{check_digit}"

    def calculate_check_digit(self, id_number):
        # 身份证号码的前17位乘数因子
        factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 对应的校验码字符
        check_digits = "10X98765432"

        sum_product = sum(int(digit) * factor for digit, factor in zip(id_number, factors))
        remainder = sum_product % 11
        return check_digits[remainder]
