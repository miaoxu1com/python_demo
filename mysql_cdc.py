import json
from datetime import datetime

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent

#由于监控捕获的模块和发送模块处理速度并不一致，发送需要耗时可能产生阻塞，而捕获数据是实时的，所以要进行解耦，使用两个进程进行处理


#1. 使用 MySQL 的触发器 + 消息队列

   # 触发器：在 MySQL 中创建一个触发器，当有数据插入目标表时，触发器将插入的事件信息写入一个专门的事件表或消息队列。

    #消息队列：使用消息队列（如 RabbitMQ、Kafka 或 Redis Stream）作为中间件，触发器将事件发布到消息队列中。

    #监控进程：一个 Python 进程作为消费者，从消息队列中订阅事件并进行处理。

#优点：

   # 解耦监控和处理逻辑。

    #消息队列可以保证事件的可靠传递和处理。

    #支持高并发和分布式处理。

#缺点：

   # 需要额外维护消息队列服务。

    #触发器的性能可能对数据库有一定影响。

#2.使用 MySQL 的 Binlog 监听
#处理进程：将捕获的事件通过进程间通信（IPC）或消息队列传递给另一个进程进行处理
#优点：

    #无需修改数据库结构（如添加触发器或事件表）。

    #实时性高，适合对实时性要求较高的场景。

    #对数据库性能影响较小。

#缺点：

    #需要解析 Binlog，实现复杂度较高。

    #需要确保 Binlog 格式和版本的兼容性。

#3.轮询 + 缓存

    轮询：监控进程定期查询目标表，检查是否有新数据插入（通过时间戳或自增 ID 判断）。

    缓存：将捕获的事件存储在缓存（如 Redis）中，供处理进程消费。

    处理进程：从缓存中读取事件并进行处理。

#优点：

    #实现简单，适合小规模场景。

    #无需依赖额外的消息队列或 Binlog 解析。

#缺点：

    #轮询方式对数据库有一定压力，尤其是高频轮询时。

    #实时性较差，取决于轮询间隔。

#4.基于 Change Data Capture (CDC) 的工具

    #CDC 工具：使用现成的 CDC 工具（如 Debezium、Maxwell）捕获 MySQL 的数据变更事件。

    #监控进程：CDC 工具将捕获的事件发布到消息队列或直接推送到 Python 进程。

    #处理进程：从消息队列或 CDC 工具的输出中读取事件并进行处理。

#优点：

    #开箱即用，功能强大。

    #支持多种数据源和目标（如 Kafka、Elasticsearch 等）。

    #适合大规模和复杂场景。

#缺点：

    #需要额外部署和维护 CDC 工具。

    #对小型项目可能过于复杂。

#5. 进程间通信 (IPC)

    #监控进程：捕获 MySQL 插入事件后，通过 IPC 机制（如管道、共享内存、Socket）将事件传递给处理进程。

    #处理进程：从 IPC 通道中读取事件并进行处理。

#优点：

   # 实现简单，适合单机多进程场景。

    #无需依赖外部服务（如消息队列）。

#缺点：

    #扩展性较差，不适合分布式场景。

    #需要处理进程间通信的同步和错误处理。

#最佳设计推荐

#根据你的需求和场景复杂度，推荐以下方案：

    #如果对实时性要求高且需要解耦：

        #使用 Binlog 监听 + 消息队列（如 Kafka 或 RabbitMQ）。

        #监控进程监听 Binlog，捕获事件后发布到消息队列，处理进程从消息队列中消费事件。

    #如果对实时性要求不高且希望简单实现：

        #使用 轮询 + 缓存（如 Redis）。

        #监控进程定期查询目标表，将新事件存储到缓存中，处理进程从缓存中读取事件。

    #如果项目规模较大且需要高可靠性：

        #使用 CDC 工具（如 Debezium）。

        #CDC 工具捕获 MySQL 变更事件并发布到消息队列，处理进程从消息队列中消费事件。

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
