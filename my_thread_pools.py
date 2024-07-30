import threadpool
import time

urls = [
    f'https://www.cnblogs.com/sitehome/p/{page}'
    for page in range(1, 20)
]
print(urls)


def myfunc(s, t):
    time.sleep(t)
    print(s)


    
# 多线程
func_vars = [(['a', 4], None), (['b', 2], None), (['c', 1], None), (['d', 3], None)]
pool = threadpool.ThreadPool(6)
tasks = threadpool.makeRequests(myfunc, args_list=func_vars)
[pool.putRequest(task) for task in tasks]
pool.wait()
