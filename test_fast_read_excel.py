# Reading Excel using Pandas
import time
from functools import wraps
from sys import getsizeof
from typing import IO, Iterator

import duckdb
import openpyxl
import pandas
import python_calamine
import tablib
from pyexcelerate import Workbook

wb = Workbook()


# def generate_test_data():
#     data = [random.randint(100, 200), random.uniform(1, 2), datetime.date(2000, 1, 1), random.choice([True, False], ),
#             "TEXT:00001111111"]
#     yield from data
#
#
# datas = []
# datas.append(["number", "decimal", "date", "boolean", "text"])
#
# data_list = []
# for _ in range(5000000):
#     datas.append(list(generate_test_data()))
#
# wb.new_sheet("sheet name", data=datas)
# wb.save("output.xlsx")

def iter_excel_pandas(file: IO[bytes]) -> Iterator[dict[str, object]]:
    yield from pandas.read_excel(file).to_dict('records')


def iter_excel_tablib(file: IO[bytes]) -> Iterator[dict[str, object]]:
    yield from tablib.Dataset().load(file).dict


def iter_excel_openpyxl(file: IO[bytes]) -> Iterator[dict[str, object]]:
    workbook = openpyxl.load_workbook(file, read_only=True)
    rows = workbook.active.rows
    headers = [str(cell.value) for cell in next(rows)]
    for row in rows:
        yield dict(zip(headers, (cell.value for cell in row)))


def iter_excel_duckdb(file: IO[bytes]) -> Iterator[dict[str, object]]:
    duckdb.install_extension('spatial')
    duckdb.load_extension('spatial')
    rows = duckdb.sql(f"""
        SELECT * FROM st_read(
            '{file.name}',
            open_options=['HEADERS=FORCE', 'FIELD_TYPES=AUTO'])
    """)
    while row := rows.fetchone():
        yield dict(zip(rows.columns, row))


def iter_excel_duckdb_execute(file: IO[bytes]) -> Iterator[dict[str, object]]:
    duckdb.install_extension('spatial')
    duckdb.load_extension('spatial')
    conn = duckdb.execute(
        "SELECT * FROM st_read(?, open_options=['HEADERS=FORCE', 'FIELD_TYPES=AUTO'])",
        [file.name],
    )
    headers = [header for header, *rest in conn.description]
    while row := conn.fetchone():
        yield dict(zip(headers, row))


def iter_excel_calamine(file: IO[bytes]) -> Iterator[dict[str, object]]:
    workbook = python_calamine.CalamineWorkbook.from_filelike(file)  # type: ignore[arg-type]
    rows = iter(workbook.get_sheet_by_index(0).to_python())
    headers = list(map(str, next(rows)))
    for row in rows:
        yield dict(zip(headers, row))


def logit():
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            #     for key, expected_value in row.items():
            #         try:
            #             value = row[key]
            #         except KeyError:
            #             print(f'🔴 "{key}" missing')
            #             continue
            #         if type(expected_value) != type(value):
            #             print(f'🔴 "{key}" expected type "{type(expected_value)}" received type "{type(value)}"')
            #         elif expected_value != value:
            #             print(f'🔴 "{key}" expected value "{expected_value}" received "{value}"')
            #         else:
            #             print(f'🟢 "{key}"')
            #     print(row)
            print(f'{end_time - start_time}s')

        return wrapped_function

    return logging_decorator


fname = 'output.xlsx'


# excel 1048576行
# 使用 Pandas 读取 Excel 290.08141565322876秒
@logit()
def read_excel_pandas(fname):
    with open(fname, 'rb') as f:
        rows = iter_excel_pandas(f)
        row = next(rows)
        print(f"pandas {getsizeof(row)} Bytes")


# read_excel_pandas(fname)


# 使用 Tablib 读取 Excel 281.5894687175751秒
@logit()
def read_excel_tablib(fname):
    with open(fname, 'rb') as f:
        rows = iter_excel_tablib(f)
        row = next(rows)
        print(f"tablib {getsizeof(row)} Bytes")


# read_excel_tablib(fname)


# 使用 Openpyxl 读取 Excel 只读模式 72.3786690235138秒  打印类型和数据
@logit()
def read_excel_openpyxl(fname):
    with open(fname, 'rb') as f:
        rows = iter_excel_openpyxl(f)
        row = next(rows)
        print(f"openpyxl {getsizeof(row)} Bytes")


# read_excel_openpyxl(fname)


# 使用 DuckDB 读取 Excel iter_excel_duckdb  131.47663760185242秒
# 使用 DuckDB 读取 Excel iter_excel_duckdb_execute 82.50024008750916秒
@logit()
def read_excel_duckdb_execute(fname):
    with open(fname, 'rb') as f:
        rows = iter_excel_duckdb_execute(f)
        row = next(rows)
        print(f"duckdb_execute {getsizeof(row)} Bytes")


# read_excel_duckdb_execute(fname)


# 使用Calamine读取 Excel 22.9017071723938秒 最快  内存占的多一些
@logit()
def read_excel_calamine(fname):
    with open(fname, 'rb') as f:
        rows = iter_excel_calamine(f)
        row = next(rows)
        print(f"calamine {getsizeof(row)} Bytes")


read_excel_calamine(fname)
