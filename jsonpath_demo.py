import time
from functools import wraps
from sys import getsizeof

import jmespath


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


data = {'foo': {'bar': 'baz'}}


@logit()
def jmespath_demo():
    res = jmespath.search('foo.bar', data)
    print(f"jmespath {getsizeof(res)} Bytes")


jmespath_demo()
