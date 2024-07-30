from threading import Thread
import time

job_list = [('a', 4), ('b', 1), ('c', 3), ('d', 2)]

# threading.Thread() 可以加()就类,这样代表初始化
# 类名和self写反会高亮显示

# 多线程步骤分解
'''
1.集成多线程类
2.重写多线程run方法
3.循环创建多线程类对象
4.开始多线程
5.阻塞多线程
threadpool 线程池是一个模块 需要安装
'''



class MyTask(Thread):
    def __init__(self, t, mystr):
        # 初始化父类对象
        super(MyTask, self).__init__()
        self.tt = t
        self.sstr = mystr

    def run(self) -> None:
        time.sleep(self.tt)
        print(self.sstr)

mythreads = None
for i in job_list:
    ssstr, ttt = i
    mythreads = MyTask(ttt, ssstr)
    mythreads.start()
    # 错误写法 看起来像是假的多线程mythreads.join()要把阻塞放在循环外边
mythreads.join()
