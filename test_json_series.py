import time
from functools import wraps
from sys import getsizeof

import cysimdjson
import json_lineage
import msgspec
import orjson
import rapidjson
import simdjson
import simplejson as sjson
import ujson

fname = "large-file.json"


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


# 耗时 0.281475305557251秒
@logit()
def read_json_by_simplejson(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        data = sjson.load(f)
        print(f"simplejson {getsizeof(data)} Bytes")


read_json_by_simplejson(fname)


# 耗时 0.27578282356262207秒
@logit()
def read_json_by_ujson(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        data = ujson.load(f)
        print(f"ujson {getsizeof(data)} Bytes")


read_json_by_ujson(fname)


# 耗时 0.2868163585662842秒
@logit()
def read_json_by_rapidjson(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        data = rapidjson.load(f)
        print(f"rapidjson {getsizeof(data)} Bytes")


read_json_by_rapidjson(fname)


# 耗时 0.12167549133300781秒
@logit()
def read_json_by_orjson(fname):
    with open(fname, mode="rb") as f:
        data = orjson.loads(f.read())
        print(f"orjson {getsizeof(data)} Bytes")


read_json_by_orjson(fname)


# 耗时 0.11330294609069824秒
@logit()
def read_json_by_json_lineage(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        data = json_lineage.load(f.read())
        print(f"json_lineage {getsizeof(data)} Bytes")


read_json_by_json_lineage(fname)

parser = cysimdjson.JSONParser()


# 耗时 0.03291010856628418秒  最快 内存最小
@logit()
def read_json_by_json_cysimdjson(fname):
    data = parser.load(fname)
    print(f"cysimdjson {getsizeof(data)} Bytes")


read_json_by_json_cysimdjson(fname)


# 耗时 0.28174495697021484秒
@logit()
def read_json_by_json_simdjson(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        data = simdjson.load(f)
        print(f"simdjson {getsizeof(data)} Bytes")


read_json_by_json_simdjson(fname)


class User(msgspec.Struct):
    """A new type describing a User"""
    name: str
    groups: set[str] = set()
    email: str | None = None


alice = User("alice", groups={"admin", "engineering"})


# 耗时 0.28174495697021484秒
@logit()
def read_json_by_json_msgspec():
    msg = msgspec.json.encode(alice)
    print(f"{getsizeof(msg)} Bytes")


read_json_by_json_msgspec()
# libpy_simdjson pip安装报错
# hyperjson 无人维护了
