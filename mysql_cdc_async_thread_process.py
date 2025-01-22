import asyncio
import json
import time
from datetime import datetime

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent

# 速度很快而且优雅
# 1. asyncio.to_thread

 #   设计目标：将阻塞任务放到线程中运行，避免阻塞事件循环。

  #  使用场景：在异步编程中处理阻塞任务（如同步 I/O 操作或短时间的 CPU 密集型任务）。

  #  编程模型：

  #      基于协程和事件循环。

  #      使用 await asyncio.to_thread(func) 将阻塞任务放到线程中运行。

   #     返回一个 awaitable 对象，可以在协程中等待任务完成。

  #  底层实现：

   #     使用线程池（concurrent.futures.ThreadPoolExecutor）执行任务。

    #    任务完成后，通过事件循环将结果返回给协程。
# 2. 多线程

 #   设计目标：实现并行执行任务，充分利用多核 CPU 的性能。

  #  使用场景：处理 CPU 密集型任务或需要并行执行的同步任务。

 #   编程模型：

  #      基于线程和锁机制。

   #     使用 threading.Thread 创建线程。

  #      需要手动管理线程的生命周期和同步。

  #  底层实现：

  #      直接使用操作系统的线程。

  #      每个线程独立运行，可以并行执行任务。

# 3. 区别
# 特性	asyncio.to_thread	  多线程 (threading.Thread)
# 设计目标	避免阻塞事件循环	    实现并行执行任务
# 编程模型	基于协程和事件循环	     基于线程和锁机制
# 使用场景	异步编程中处理阻塞任务	  处理 CPU 密集型任务或并行任务
# 线程管理	自动管理线程池	       需要手动管理线程
# 性能	适合 I/O 密集型任务	       适合 CPU 密集型任务
# 复杂性	更简单，适合与异步代码集成	 更复杂，需要处理线程同步和资源竞争
# 底层实现	使用线程池执行任务	       直接使用操作系统的线程


# 4. 实际原理
#（1）asyncio.to_thread 的原理

 #   asyncio.to_thread 的底层使用了 concurrent.futures.ThreadPoolExecutor，它是一个线程池。

  #  当调用 await asyncio.to_thread(func) 时：

  #      将 func 提交到线程池中执行。

 #       在任务完成之前，事件循环可以继续运行其他协程。

 #       任务完成后，通过事件循环将结果返回给协程。

#（2）多线程的原理

 #   多线程直接使用操作系统的线程。

 #   每个线程独立运行，可以并行执行任务。

  #  需要手动管理线程的生命周期和同步（如使用 threading.Thread 和 threading.Lock）

   # 使用 asyncio.to_thread：

    #    如果你正在编写异步代码，并且需要处理阻塞任务。

    #    如果你不想手动管理线程。

    #    适合 I/O 密集型任务或短时间的 CPU 密集型任务。

   # 使用多线程：

    #    如果你需要并行执行任务，充分利用多核 CPU 的性能。

     #   如果你需要更精细地控制线程的行为（如线程优先级、线程间通信等）。

     #   适合 CPU 密集型任务或需要并行执行的同步任务。

# MySQL 连接配置
mysql_settings = {
    'host': '',
    'port': ,
    'user': '',
    'passwd': ''
}

# 记录解析位置的文件
position_file = 'binlog_position.json'


def load_position():
    """加载上次解析的位置"""
    try:
        with open(position_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'log_file': None, 'log_pos': None}


def save_position(log_file, log_pos):
    """保存当前解析的位置"""
    with open(position_file, 'w') as f:
        json.dump({'log_file': log_file, 'log_pos': log_pos}, f)


# 加载上次解析的位置
position = load_position()
log_file = position.get('log_file')
log_pos = position.get('log_pos')


# 获取当天的起始时间
def get_today_start_time():
    today = datetime.now().date()
    return datetime(today.year, today.month, today.day)


# 创建 BinLogStreamReader 对象
stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    server_id=100,  # 唯一 ID
    blocking=True,  # 阻塞模式，实时监听
    only_events=[WriteRowsEvent],  # 只监听插入事件
    only_schemas=['target_cis'],  # 只监听指定库
    only_tables=['u_user_allot_email_log'],  # 只监听指定表
    resume_stream=True,
    log_file=log_file,  # 从上次解析的文件开始
    log_pos=log_pos  # 从上次解析的位置开始
)
data_queue = asyncio.Queue(maxsize=1000)  # 设置队列的最大容量


def binlog_monitor():
    # 监听 BINLOG
    try:
        for binlogevent in stream:
            print(50 * "=")
            print(f"当前binlog file是{stream.log_file}")
            print(f"当前binlog file pos是{stream.log_pos}")
            # 检查事件类型
            event_time = datetime.fromtimestamp(binlogevent.timestamp)  # 获取事件时间戳
            today_start = get_today_start_time()
            # 检查事件是否发生在当天
            if event_time >= today_start:
                print(f"发现新数据插入，表: {binlogevent.table}")
                print(f"事件时间戳: {event_time}")
                for row in binlogevent.rows:
                    email_addr = row['values']['UNKNOWN_COL3']
                    # 记录插入的数据
                    print("插入的邮箱地址:", email_addr)
                    print(f"监控进程：捕获到插入事件，数据已存入缓存 -> {email_addr}")
                    data_queue.put_nowait(email_addr)
                    # get_email_info(user_no)
                    # 可以将数据写入文件或数据库
                    # with open('insert_log.txt', 'a') as f:
                    #     f.write(f"表: {binlogevent.table}, 数据: {row['values']}\n")
                    print(50 * "#")
                save_position(stream.log_file, stream.log_pos)
    finally:
        # 关闭流
        stream.close()


# 消费协程（消费者）
def data_consumer():
    while True:
        # 读取缓存中的最新数据

        # 模拟数据处理逻辑
        try:
            data = data_queue.get_nowait()  # 超时 5 秒
            print(f"处理进程：读取到数据 -> {data}")
            # 这里可以替换为实际的数据处理逻辑
            print(f"处理进程：正在处理数据 -> {data}")
            time.sleep(3)  # 模拟处理耗时
            print(f"处理进程：数据处理成功 -> {data}")
            print(50*"*")
            # 标记任务完成
            data_queue.task_done()
        except asyncio.QueueEmpty:
            time.sleep(4)
            # 如果处理失败，可以将数据重新放回缓存


# 主函数
async def main():
    # 启动监控协程和消费协程
    monitor_task = asyncio.to_thread(binlog_monitor)
    consumer_task = asyncio.to_thread(data_consumer)

    # 等待任务完成
    await asyncio.gather(monitor_task, consumer_task)


if __name__ == "__main__":
    # 启动监控进程
    asyncio.run(main())
