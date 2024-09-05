import time
from datetime import datetime, timedelta
from functools import wraps
from sys import getsizeof
from zoneinfo import ZoneInfo

import pendulum
from whenever import (
    # Explicit types for different use cases
    Instant, LocalDateTime,
)


# 根据pycharm提示导入包即可

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


# 耗时 0.0214996337890625s
@logit()
def date_time_demo():
    bedtime = datetime(2023, 3, 25, 22, tzinfo=ZoneInfo("Europe/Paris"))
    res = bedtime + timedelta(hours=8)
    print(f"date_time {getsizeof(res)} Bytes")


date_time_demo()


# 耗时 0.001100301742553711s
@logit()
def whenever_demo():
    now = Instant.now()
    now.to_tz("Europe/Paris")
    party_invite = LocalDateTime(2023, 10, 28, hour=22)
    party_starts = party_invite.assume_tz("Europe/Amsterdam", disambiguate="earlier")
    party_starts.add(hours=6)
    now.format_rfc2822()
    now.py_datetime()
    print(f"date_time {getsizeof(party_starts)} Bytes")


whenever_demo()


# 耗时
@logit()
def pendulum_demo():
    now = now_in_paris = pendulum.now('Europe/Paris')
    now_in_paris.in_timezone('UTC')
    tomorrow = pendulum.now().add(days=1)
    last_week = pendulum.now().subtract(weeks=1)
    past = pendulum.now().subtract(minutes=2)
    past.diff_for_humans()
    delta = past - last_week
    pendulum.datetime(2013, 3, 31, 2, 30, tz='Europe/Paris')
    just_before = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999, tz='Europe/Paris')
    just_before.add(microseconds=1)
    print(f"date_time {getsizeof(tomorrow)} Bytes")


pendulum_demo()
