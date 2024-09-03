# Wring Excel using pyexcelerate
import datetime
import random
import time

from pyexcelerate import Workbook

wb = Workbook()

# pyexcelerate 100k 写入excel  35.083603382110596秒
def generate_test_data():
    data = [random.randint(100, 200), random.uniform(1, 2), datetime.date(2000, 1, 1), random.choice([True, False], ),
            "TEXT:00001111111"]
    yield from data


start_time = time.time()
datas = []
datas.append(["number", "decimal", "date", "boolean", "text"])

data_list = []
for _ in range(1000000):
    datas.append(list(generate_test_data()))

wb.new_sheet("sheet name", data=datas)
wb.save("output.xlsx")
end_time = time.time()
print(end_time - start_time)
