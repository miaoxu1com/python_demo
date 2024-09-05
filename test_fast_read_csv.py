import time
from functools import wraps
from sys import getsizeof

import numpy as np
import pandas as pd
import polars as pl


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


fname = "output.csv"


# 耗时0.4268953800201416秒
@logit()
def pandas_read_csv():
    data = pd.read_csv(fname,
                       header=0,
                       index_col=None)
    print(f"pandas default {getsizeof(data)} Bytes")
    return data


# 装饰器 中使用闭包函数，然后在函数中一层层返回，装饰器像是洋葱，洋葱要从外一层层的剥  装饰器是最外层的，所以就是先执行最外层装饰器函数，装饰器函数又引用了自定义的函数
# yield 是挂起返回 return是中断返回
pandas_read_csv()


# 耗时0.0763709545135498秒
@logit()
def pandas_read_csv_by_pyarrow():
    data = pd.read_csv(fname,
                       engine="pyarrow",
                       header=0,
                       index_col=None)
    print(f"pandas pyarrow {getsizeof(data)} Bytes")
    return data


pandas_read_csv_by_pyarrow()


# 耗时3.424750566482544秒
@logit()
def pandas_read_csv_by_python():
    data = pd.read_csv(fname,
                       engine="python",
                       header=0,
                       index_col=None)
    print(f"pandas python {getsizeof(data)} Bytes")
    return data


pandas_read_csv_by_python()


# 耗时1.9833924770355225秒
@logit()
def pandas_read_csv_by_python_fwf():
    data = pd.read_csv(fname,
                       engine="python-fwf",
                       header=0,
                       index_col=None)
    print(f"pandas python_fwf {getsizeof(data)} Bytes")
    return data


pandas_read_csv_by_python_fwf()


# 耗时 0.5475084781646729秒 解包就是csv列，不解包就是csv行
@logit()
def numpy_read_csv():
    data = np.array(np.loadtxt(fname, unpack=True, encoding='utf-8', skiprows=1, dtype=str))
    print(f"numpy  {getsizeof(data)} Bytes")


numpy_read_csv()


# 耗时0.037897348403930664秒
@logit()
def polars_lazy_read_csv():
    lazy_df = pl.scan_csv(fname)

    # 定义数据处理操作
    result_df = (
        lazy_df.select(["number", "decimal", "date", "boolean", "text"])

    )

    # 收集并显示结果
    result_df.collect()
    print(f"polars_lazy {getsizeof(result_df)} Bytes")


polars_lazy_read_csv()


# 耗时0.0554041862487793秒  最快 内存最小
@logit()
def polars_lazy_streaming_read_csv():
    lazy_df = pl.scan_csv(fname)

    # 定义数据处理操作
    result_df = (
        lazy_df.select(["number", "decimal", "date", "boolean", "text"])

    )

    # 懒惰操作并使用流式读取收集结果
    data = result_df.collect(streaming=True)
    print(f"polars_lazy_streaming  {getsizeof(data)} Bytes")


polars_lazy_streaming_read_csv()


def vaex_lazy_read_csv():
    # df = vaex.open(fname, memory_map=True)
    pass
    # 显示结果
    # print(df)
