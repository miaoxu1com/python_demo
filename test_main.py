import hashlib
import json
import time
import uuid
from faker import Faker
from generate_fake_data import *
from multi_thread_file_write import *


def dataclass
    pass


def generate_test_data_numbers():
    fake = Faker('zh_CN')  # 使用中文地区设置
    fake.add_provider(IDCardProvider)
    id_no = fake.id_card_number("河南省")
    phone_numbers = fake.phone_number()
    return phone_numbers, id_no


def MyDataClass():
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.phone_number, self.id_no = generate_test_data_numbers()


# 生成随机数据
def generate_data(num_rows):
    data = []
    for _ in range(num_rows):
        row = MyDataClass()
        data.append(row)
    return data


def main():
    start_task(thread_write_csv)


# 线程函数
def thread_write_csv(index):
    data = generate_data(200)
    file_name = f'thread_{index}.csv'
    write_to_csv(file_name, data)
    print(f"Thread {index} finished writing to {file_name}")
