import time
from multiprocessing.dummy import Pool
from functools import partial

# 使用线程池的方式执行
start_time = time.time()


def get_page(tt):
    """
    元组的妙用-传递一个元祖进入线程池的方法然后再进行解包
    列表不能解包，元祖才有这个特性
    zip就是把多个循环对象进行重组成一个新的元组
    """
    t, mystr = tt
    time.sleep(t)  # 模拟阻塞
    print('download success: ', mystr)


name_list = [(1, 'a'), (4, 'b'), (2, 'c'), (3, 'd')]
# 实例化一个线程池对象
pool = Pool(4)  # 开辟4个线程
# 将列表中的每一个元素传递给get_page执行
# func = partial(get_page, name_list)
pool.map(get_page, name_list)
end_time = time.time()
print(end_time - start_time)
