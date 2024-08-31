import copy
import datetime
import getpass
import logging
import os

import keyring
import requests
import threadpool
from sqlalchemy import create_engine, Column, Integer, String, DateTime, inspect, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 打包成exe 无法着色  而且一定要把打包的程序放在依赖文件目录下否则闪退
def init_passwd():
    user_name = input("input your user name：")
    print("your user name is " + user_name)
    pwd = getpass.getpass('input your password：')
    keyring.set_password('itone', user_name, pwd)
    if os.path.exists('username.txt') is True:
        return False
    else:
        with open('username.txt', 'a') as fl:
            fl.write(user_name)


class Task:
    def __init__(self, us_business_no_list=None, user_name=None, password=None, task_business_no_list=None):
        self.session = requests.session()
        self.session.verify = False
        self.us_business_no = us_business_no_list
        self.user_name = user_name
        self.passwd = password
        self.login()
        self.us_dto = None
        self.task_dto = {
           
        }
        self.task_update_dto = {
           
        }
        self.task_business_no_list = task_business_no_list
        self.query_need_update_dto = {
           
        }

    def query_us_list_by_pi_name(self):
        url = url地址
        json_str = {
           
        }
        response = self.session.post(url=url, json=json_str)
        result = response.json()['result']['requirements']
        # 如果是复合结构判断要用isinstance type判断不准确
        return result if isinstance(result, list) else None

    def login(self):
        url = ""
        form_data = {
            "loginMethod": "login",
            "uid": self.user_name,
            "password": self.passwd,
            "actionFlag": "loginAuthenticate"
        }
        self.session.post(url, data=form_data, verify=False)

    def query_us_by_business_no(self):
        us_dto = []
        url = url地址
        domain = {}
        json_str = {
          
        }
        if self.us_business_no is None:
            return None
        else:
            us_dto = []

            # for i in range(len(self.us_business_no)):
            #     json_str['reqQueryCondition']['businessNo'] = self.us_business_no[i]
            #     reponse = self.session.post(url=url, json=json_str)
            #     us_dto.append(reponse.json()['result']['requirements'][0])

            def thread_request(data=None):
                request_str = copy.deepcopy(json_str)
                request_str['reqQueryCondition']['businessNo'] = data
                reponse = self.session.post(url=url, json=request_str)
                us_dto.append(reponse.json()['result']['requirements'][0])

            pool = threadpool.ThreadPool(10)
            tasks = threadpool.makeRequests(thread_request, args_list=self.us_business_no)
            [pool.putRequest(task) for task in tasks]
            pool.wait()
            return us_dto if us_dto is not None else None

    # 创建task
    def save_task(self):
        self.us_dto = self.query_us_by_business_no() or self.query_us_list_by_pi_name()
        url = url地址
        sqm = SqliteManger()
        test_plan = sqm.session.query(TaskPlan).filter(TaskPlan.is_default == 1).all()

        def threads_request(us_dto):
            test_case = copy.deepcopy(self.task_dto)
            test_case['key1'] = us_dto['value']
            test_case['key1'] = us_dto['value']
            test_case['key1'] = us_dto['value']
            test_case['key1'] = us_dto['value']
            test_case['key1'] = us_dto['value']
            test_case['key1'] = us_dto['value']
            test_case['key1'] = us_dto['value']
            test_case['key1'] = 0
            test_case['key1'] = us_dto['value']
            test_case['key1'] = self.user_name
            test_case['key1'] = self.user_name
            for k in test_plan:
                test_case['key1'] = k.work_time
                test_case['key1'] = k.work_time
                test_case['key1'] = k.prefix + us_dto['key1']
                json_str = [test_case]
                # print(json_str)
                response = self.session.post(url=url, json=json_str)
                print(response.content.decode("utf8"))
                if response.json()['status'] != 'ok':
                    return 0

        pool = threadpool.ThreadPool(10)
        tasks = threadpool.makeRequests(threads_request, self.us_dto)
        [pool.putRequest(task) for task in tasks]
        pool.wait()


def login_init():
    #  初始化us列表,登录名，密码
    service_name = 'itone'
    username = None
    with open('username.txt', 'r') as f:
        username = f.read()
    passwd = keyring.get_password(service_name, username)
    login = (username, passwd)
    return login


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
        m = int(i[4:5])  # 日志的月份
        today_y = int(del_log_year)  # 今天的年份
        y = int(i[0:4])  # 日志的年份
        today_d = int(del_log_d)
        d = int(i[7:8])
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



def task_init():
    # us_name列表
    us_business_no = []

    # task_name列表
    task_business_no = []
    login = login_init()
    my_task = Task(us_business_no_list=us_business_no, user_name=login[0], password=login[1],
                   task_business_no_list=task_business_no)
    return my_task


# 定时任务自动更新
def update_task_by_id():
    my_task = task_init()
    url = url地址
    update_task = query_need_update_task()
    update_task_list = update_task['key1']['key2']
    logging.basicConfig(format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                        filename=datetime.datetime.strftime(datetime.datetime.now(), "%Y%d%m") + "_run.log",
                        filemode="a",
                        level=logging.DEBUG)
    if len(my_task.task_business_no_list) == 0 and update_task_list == 0:
        logging.info("task已全部更新")
    update_task_list = update_task_list if len(my_task.task_business_no_list) > 0 else update_task_list[0:1]
    data = []
    for i in range(len(update_task_list)):
        task_update_dto = copy.deepcopy(my_task.task_update_dto)
        task_update_dto['key1'] = update_task_list[i]['key1']
        task_update_dto['key1'] = update_task_list[i]['key1']
        task_update_dto['key1'] = update_task_list[i]['key1']
        task_update_dto['key1'] = update_task_list[i]['key1']
        task_update_dto['key1'] = 0
        data.append(task_update_dto)

    response = my_task.session.put(url, json=data)
    if response.json()['status'] == 'ok':
        print(response.content.decode("utf8"))
        logging.info(str(data) + "|" + str(response.content.decode("utf8")))
        print("更新成功")


# 查询状态是初始化的task
def query_need_update_task():
    my_task = task_init()
    url = url地址
    task_business_no_len = len(my_task.task_business_no_list)
    count = 0
    if task_business_no_len > 0:
        task_list = []
        for i in range(task_business_no_len):
            my_task.query_need_update_dto['key1'] = my_task.task_business_no_list[i]
            response = my_task.session.post(url, json=my_task.query_need_update_dto)
            if response.json()['status'] == 'ok':
                count += 1
                try:
                    task_list.append(response.json()['key1']['key2'][0])
                except Exception:
                    print("未查到初始化的Task")
                    return
        temp = copy.deepcopy(response.json())
        temp['key1']['key2'] = task_list
        temp['key1']['key2'] = count
    else:
        response = my_task.session.post(url, json=my_task.query_need_update_dto)
        temp = response.json()
    return temp


def print_menu():
    menue = ["创建Task", "更新工作量", "查看Task拆分方案", "添加Task拆分方案", "设置默认方案", "设置task工作量方案", "退出"]
    menue_title = ['一级菜单']
    print_str_len = 32
    # print(print_str_len * "\033[32;1m*")
    # 要打包exe  不支持着色显示
    print(print_str_len * "*")
    print(menue_title[0])
    print(print_str_len * "*")
    count = 0
    print_str = "*"
    for v in menue:
        count = count + 1
        print(str(count) + "." + v)
    print(print_str_len * print_str)


def app_main():
    print_menu()
    sql_mng = SqliteManger()
    my_task = task_init()
    while 1:
        key = input("请输入你的操作：")
        # 创建Task
        if key == '1':
            my_task.query_us_by_business_no()
            my_task.save_task()
            print_menu()
        # 更新工作量
        elif key == '2':
            if query_need_update_task() is None:
                print_menu()
            else:
                update_task_by_id()
        # 查看Task拆分方案
        elif key == '3':
            # 查询数据
            sql_mng.query()
            print_menu()
        # 添加Task拆分方案
        elif key == '4':
            query_obj = sql_mng.query()
            task_list = []
            while 1:
                name = input("请输入task方案名称：")
                prefix = input("请输入task拆分前缀：")
                suffix = input("请输入task拆分后缀：")
                task_list.append(TaskPlan(name=name,
                                          example=prefix + 'us_name' + suffix,
                                          no=query_obj.first().no + 1,
                                          prefix=prefix,
                                          suffix=suffix,
                                          create_by=login_init()[0],
                                          create_time=datetime.datetime.now())
                                 )

                key = input("1.继续添加一拆多 2.完成添加 \n")
                if key == '2':
                    break
            sql_mng.add(task_plan=task_list)
            print_menu()
        # 设置默认方案
        elif key == '5':
            sql_mng.query()
            no = input("请选择默认方案的编号：")
            sql_mng.update(no=no, update_default={"is_default": 1}, update_no_default={"is_default": 0})
            print_menu()
        # 设置task工作量方案
        elif key == '6':
            sql_mng.query()
            key = input("请选择更新工作量的方案：")
            work_time_default = input("请输入预估工作量：")
            sql_mng.session.query(TaskPlan).filter(TaskPlan.no == key).update({"work_time": work_time_default})
            sql_mng.close_session()
            print_menu()
        # 退出
        elif key == '7':
            exit()
        # 添加初始化数据
        elif key == '8':
            sql_mng.init_data()
            print_menu()


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


if __name__ == '__main__':
    app_main()
    # tstart = datetime.datetime.now()
    # mytask = task_init()
    # mytask.save_task()
    # print(datetime.datetime.now() - tstart)

