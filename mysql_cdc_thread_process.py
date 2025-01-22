import json
import queue
import threading
from datetime import datetime
import time
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent

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
data_queue = queue.Queue(maxsize=1000)  # 设置队列的最大容量


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
                    data_queue.put(email_addr)
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
        # 模拟数据处理逻辑
        try:
            data = data_queue.get(timeout=5)  # 超时 5 秒
            print(f"处理进程：读取到数据 -> {data}")
            # 这里可以替换为实际的数据处理逻辑
            print(f"处理进程：正在处理数据 -> {data}")
            time.sleep(3)  # 模拟处理耗时
            print(f"处理进程：数据处理成功 -> {data}")
            # 标记任务完成
            data_queue.task_done()
        except queue.Empty:
            print("队列为空等待新数据")
            # 如果处理失败，可以将数据重新放回缓存


if __name__ == "__main__":
    # 启动监控线程和消费线程
    monitor_thread = threading.Thread(target=binlog_monitor, name="MonitorThread")
    consumer_thread = threading.Thread(target=data_consumer, name="ConsumerThread")
    monitor_thread.start()
    consumer_thread.start()
    # 等待线程结束
    monitor_thread.join()
    consumer_thread.join()
