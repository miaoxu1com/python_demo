# Wring Excel using pyexcelerate
import datetime
import random
import time
from functools import wraps
from sys import getsizeof

import numpy as np
from pyexcelerate import Workbook as pyexcelWorkbook
from pyfastexcel import StreamWriter


def logit():
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            print(end_time - start_time)

        return wrapped_function

    return logging_decorator


# pyexcelerate 100k 写入excel  35.083603382110596秒
def generate_test_data():
    data = [random.randint(100, 200), random.uniform(1, 2), datetime.date(2000, 1, 1), random.choice([True, False], ),
            "TEXT:00001111111"]
    yield from data


@logit()
def write_excel_by_pyexcelerate():
    wb = pyexcelWorkbook()
    datas = []
    datas.append(["num", "decimal", "date", "boolean", "text"])
    [datas.append(list(generate_test_data())) for _ in np.arange(1e6)]
    wb.new_sheet("sheet name", data=datas)
    wb.save("output.xlsx")
    print(f"pyexcelerate {getsizeof(datas)} Bytes")


# write_excel_by_pyexcelerate()


def prepare_data():
    datas = []
    headers = ["num", "decimal", "date", "boolean", "text"]
    [datas.append(list(generate_test_data())) for _ in np.arange(1e6)]
    records = [
        {header: str(value) for header, value in zip(headers, row)}
        for row in datas
    ]
    print(f"pyfastexcel {getsizeof(records)} Bytes")
    return records


class PyFastExcelStreamExample(StreamWriter):
    def create_excel(self) -> bytes:
        self._set_header()
        # 设置文件源数据
        self.set_file_props('Creator', 'Hello')
        self._create_single_header()
        self._create_body()
        return self.read_lib_and_create_excel()

    def _set_header(self):
        self.headers = list(self.data[0].keys())

    def _create_single_header(self):
        [self.row_append(h) for h in self.headers]
        self.create_row()

    def _create_body(self) -> None:
        for row in self.data:
            for h in self.headers:
                # 使用表头关键字取值追加到行
                self.row_append(row[h])
            self.create_row()


@logit()
def pyfastexcel_create_excel():
    data = prepare_data()
    stream_writer = PyFastExcelStreamExample(data)
    excel_bytes = stream_writer.create_excel()
    file_path = 'pyexample_stream.xlsx'
    stream_writer.save(file_path)


pyfastexcel_create_excel()
