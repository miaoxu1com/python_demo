import time
from functools import wraps
from sys import getsizeof

import anyconfig
import pytomlpp
import qtoml
import rtoml
import toml
import tomli
import tomlkit


def logit():
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            print(f'{end_time - start_time}s')

        return wrapped_function

    return logging_decorator


fname = "example.toml"


# tomli_w 只支持写不参加bench
# 耗时
@logit()
def read_toml_by_anyconfig(fname):
    conf = anyconfig.load(fname)
    print(f"anyconfig {getsizeof(conf)} Bytes")


read_toml_by_anyconfig(fname)


# 耗时
@logit()
def read_toml_by_toml(fname):
    with open(fname, mode="r") as fp:
        conf = toml.load(fp)
        print(f"toml {getsizeof(conf)} Bytes")


read_toml_by_toml(fname)


# 耗时
@logit()
def read_toml_by_tomlkit(fname):
    with open(fname, mode="rb") as fp:
        conf = tomlkit.load(fp)
        print(f"tomlkit {getsizeof(conf)} Bytes")


read_toml_by_tomlkit(fname)


# 耗时 使用了缓存，二次读取花费时间是0，其他的没使用缓存
@logit()
def read_toml_by_rtoml(fname):
    with open(fname, mode="r") as fp:
        conf = rtoml.load(fp)
        print(f"rtoml {getsizeof(conf)} Bytes")


read_toml_by_rtoml(fname)


# 耗时
@logit()
def read_toml_by_qtoml(fname):
    with open(fname, mode="r") as fp:
        conf = qtoml.load(fp)
        print(f"qtoml {getsizeof(conf)} Bytes")


read_toml_by_qtoml(fname)


# 耗时 pytomlpp使用了缓存
@logit()
def read_toml_by_pytomlpp(fname):
    with open(fname, mode="rb") as fp:
        conf = pytomlpp.load(fp)
        print(f"pytomlpp {getsizeof(conf)} Bytes")


read_toml_by_pytomlpp(fname)


# 耗时
@logit()
def read_toml_by_pytomlpp(fname):
    with open(fname, "rb") as f:
        tomli_dict = tomli.load(f)
        print(f"tomli {getsizeof(tomli_dict)} Bytes")


read_toml_by_pytomlpp(fname)
