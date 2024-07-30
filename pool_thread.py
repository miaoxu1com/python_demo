import copy
import datetime
import getpass
import logging
import os
import time

import keyring
import requests
import threadpool
from lxml import etree
from sqlalchemy import create_engine, Column, Integer, String, DateTime, inspect, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 控制台用制表符显示表格格式数据

class Task:

    def threads_request_remove_list(self, us_dto):
        get_task_url = ''
        get_ir_url = ''
        payload = {
            "id": "",
            "_": round(time.time() * 1000)
        }
        params = {
            "_": round(time.time() * 1000)
        }
        json_str = {
            "domain": "",
            "type": "US",
            "itemId": us_dto['id']
        }
        res = self.session.post(url=get_ir_url, params=params, json=json_str)
        if isinstance(res.json()['result'], list) and len(res.json()['result']) > 0:
            for k in res.json()['result']:
                if isinstance(k['items'], list) and len(k['items']) > 0:
                    for i in k['items']:
                        payload['id'] = i['dependedBy']
                        res = self.session.get(url=get_task_url, params=payload)
                        if isinstance(res.json()['result'], list) and len(res.json()['result']) > 0:
                            for z in res.json()['result']:
                                if z['type'] == 'Task' and z['owner'] == 'id':
                                    print("谁" + z['owner'], "编号：" + us_dto['businessNo'] + "被怎么了",
                                          "US ID：" + us_dto['id'],
                                          "关联了：" + z['businessNo'])
                                    self.us_dto.remove(us_dto)
                                    return 0
                                else:
                                    return 0
                        else:
                            return 0
                else:
                    return 0

    def threads_request_create_task(self, us_dto):
        sqm = SqliteManger()
        url = ""
        test_plan = sqm.session.query(TaskPlan).filter(TaskPlan.is_default == 1).all()
        test_case = copy.deepcopy(self.task_dto)
        test_case['description'] = us_dto['description']
        test_case['pi'] = us_dto['pi']
        test_case['iterateId'] = us_dto['iterateId']
        test_case['iterateName'] = us_dto['iterateName']
        test_case['piName'] = us_dto['piName']
        test_case['domainName'] = us_dto['domainName']
        test_case['domain'] = us_dto['domain']
        test_case['sumWorkloadManday'] = 0
        test_case['dependedOn'] = us_dto['id']
        test_case['creator'] = self.user_name
        test_case['owner'] = self.user_name
        for k in test_plan:
            test_case['workload'] = k.work_time
            test_case['remainWorkloadManday'] = k.work_time
            test_case['name'] = k.prefix + us_dto['name']
            json_str = [test_case]
            # print(json_str)
            response = self.session.post(url=url, json=json_str)
            print(response.content.decode("utf8"))
            if response.json()['status'] != 'ok':
                return 0

    def save_task(self):
        # 编号优先
        # self.us_dto = self.query_us_by_business_no() or self.query_us_list_by_pi_name()
        # 优先
        self.us_dto = self.query_us_list_by_pi_name() or self.query_us_by_business_no()

        print("总共：" + str(len(self.us_dto)) + "条")
		# 复用线程池
        pool = threadpool.ThreadPool(10)
        tasks = threadpool.makeRequests(self.threads_request_remove_list, self.us_dto)
        [pool.putRequest(task) for task in tasks]
        pool.wait()
		# 两次线程池处理了两个事情
        tasks = threadpool.makeRequests(self.threads_request_create_task, self.us_dto)
        [pool.putRequest(task) for task in tasks]
        pool.wait()

    
log_dir = os.path.join(os.getcwd(), 'log')


def clean_log():
    path = os.path.join(os.getcwd(), 'log')
    log_date = (datetime.datetime.now() - datetime.timedelta(days=7))
    del_log_year = log_date.year
    del_log_mon = log_date.month
    del_log_d = log_date.day

    # 遍历目录下的所有日志文件 i是文件名
    for i in os.listdir(log_dir):
        file_path = os.path.join(path, i)  # 生成日志文件的路径
        # 获取日志的年月，和今天的年月
        today_m = int(del_log_mon)  # 今天的月份
        m = int(i[4:6])  # 日志的月份
        today_y = int(del_log_year)  # 今天的年份
        y = int(i[0:4])  # 日志的年份
        today_d = int(del_log_d)
        d = int(i[6:8])
        # 对上个月的日志进行清理，即删除。
        if m < today_m:
            if os.path.exists(file_path):  # 判断生成的路径对不对，防止报错
                os.remove(file_path)  # 删除文件
        elif y < today_y:
            if os.path.exists(file_path):
                os.remove(file_path)
        elif d < today_d:
            if os.path.exists(file_path):
                os.remove(file_path)


Base = declarative_base()


class TaskPlan(Base):
    __tablename__ = 'task_plan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    example = Column(String(100))
    no = Column(Integer)
    prefix = Column(String(20))
    suffix = Column(String(20))
    create_by = Column(String(20))
    create_time = Column(DateTime)
    is_default = Column(Integer, nullable=True)
    work_time = Column(Integer)


class SqliteManger:

    def __init__(self):
        self.engine = create_engine('sqlite:///task.db?check_same_thread=False', echo=False)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.insp = inspect(self.engine)

    # 创建表
    def create_table(self):
        Base.metadata.create_all(self.engine, checkfirst=True)
        print(self.insp.get_table_names())

    # 查询表列
    def query_table_colum(self):
        md = MetaData()
        table = Table('task_plan', md, autoload=True, autoload_with=self.engine)
        columns = table.c
        print([c.name for c in columns])

    # 删除表
    def delete_table(self):
        print(self.insp.get_table_names())
        Base.metadata.drop_all(self.engine)
        print(self.insp.get_table_names())

    # 关闭会话链接
    def close_session(self):
        self.session.commit()
        self.session.close()

    # 添加数据
    def add(self, task_plan=None):
        self.session.add_all(task_plan)
        SqliteManger.close_session(self)

    # 更新数据
    def update(self, **kwargs):
        self.session.query(TaskPlan).filter(not (TaskPlan.no == kwargs['no'])).update(kwargs['update_no_default'])
        self.session.query(TaskPlan).filter(TaskPlan.no == kwargs['no']).update(kwargs['update_default'])
        SqliteManger.close_session(self)

    # 初始化表数据
    def init_data(self):
        self.delete_table()
        self.create_table()
        self.session.add_all([
            TaskPlan(name='task一拆一', example='【方案设计_测试用例编写_测试执行】+us_name', no=1, prefix='【方案设计_测试用例编写_测试执行】',
                     suffix=None,
                     create_by=login_init()[0],
                     create_time=datetime.datetime.now(), work_time=32),
            TaskPlan(name='task一拆三', example='【方案设计】+us_name', no=2, prefix='【方案设计】', suffix=None,
                     create_by=login_init()[0],
                     create_time=datetime.datetime.now(), is_default=1, work_time=16),
            TaskPlan(name='task一拆三', example='【测试用例编写】+us_name', no=2, prefix='【测试用例编写】', suffix=None,
                     create_by=login_init()[0],
                     create_time=datetime.datetime.now(), is_default=1, work_time=16),
            TaskPlan(name='task一拆三', example='【测试执行】+us_name', no=2, prefix='【测试执行】', suffix=None,
                     create_by=login_init()[0],
                     create_time=datetime.datetime.now(), is_default=1, work_time=16)
        ])
        SqliteManger.close_session(self)

    # 查询数据
    def query(self):
        data = self.session.query(TaskPlan).order_by(TaskPlan.no.desc())
        print(2 * " " + "方案名", "\t\t例子", "\t\t方案编号", "默认方案", "工作量")
        for i in data.all():
            print(i.name, "|", i.example, "|", i.no, "|", "是" if i.is_default == 1 else "否", "|", i.work_time)
        return data
