import json
from datetime import datetime

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent

#由于监控捕获的模块和发送模块处理速度并不一致，发送需要耗时可能产生阻塞，而捕获数据是实时的，所以要进行解耦，使用两个进程进行处理

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

print(log_file,log_pos)
# 创建 BinLogStreamReader 对象
stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    server_id=100,  # 唯一 ID
    blocking=True,  # 阻塞模式，实时监听
    only_events=[WriteRowsEvent],  # 只监听插入事件
    only_schemas=['target_lps'],  # 只监听指定库
    only_tables=['ap_appl'],  # 只监听指定表
    resume_stream=True,
    log_file=log_file,  # 从上次解析的文件开始
    log_pos=log_pos  # 从上次解析的位置开始
)


# 监听 BINLOG
try:
    for binlogevent in stream:
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
                    # 记录插入的数据
                    print("插入的数据:", row['values'])
                    # 可以将数据写入文件或数据库
                    # with open('insert_log.txt', 'a') as f:
                    #     f.write(f"表: {binlogevent.table}, 数据: {row['values']}\n")
                save_position(stream.log_file, stream.log_pos)
finally:
    # 关闭流
    stream.close()
