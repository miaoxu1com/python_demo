from dataclasses import dataclass, asdict, astuple
from datetime import datetime

import attr
from pydantic import BaseModel, field_validator


# https://www.modb.pro/db/412679

@dataclass
class Person:
    name: str
    age: int


'''
需要做数据验证时，就要用数据验证工具库，而数据验证class又是最佳的数据容器
类具有方法，可以实验对数据验证的模块化处理，让代码更易于阅读和维护，而dataclass
又易于使用和更优雅所以就是一个比较好用的数据工具，类就是对实例的抽象，
类的方式可以让实例之间产生关系，还可以提供接口方便修改数据，控制数据权限
定义接口
'''

Person1 = Person("John", 50)
asdict(Person1)
# 获取值和名，函数可以将对象转成 dict
print(asdict(Person1))
# 只获取值，函数可以将对象转成tupple
print(astuple(Person1))


# https://blog.csdn.net/weixin_49520696/article/details/134172661 泛型属于类型提示
# attrs 还具备 slots 和 programmatic creation

# 从上面的例子，不难看出 pydantic 有下面几个问题：
#
#     pydantic 不支持位置参数
#     pydantic 的输出有点奇怪，没有带上类名
#     pydantic 不支持 slots
#     和 programmatic creation
#     pydantic 不支持 Collection 类型
#
# 在参考文章中还提到了 pydantic 对 unions 的策略有问题，不容易定制，并且对定制的（非）结构化的支持很弱。
#
# 所以如果有复杂的需求的话，建议使用 attrs
# ，只是想简单的呈现对象的属性的话，可以考虑用 dataclasses

class Book(BaseModel):
    publish_date: datetime

    @field_validator("publish_date", mode="before")
    def conver_to_datetime(cls, user_input):
        if isinstance(user_input, str):
            return datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
        elif isinstance(user_input, datetime):
            print(user_input)
            return user_input
        raise TypeError("不支持的参数类型，仅支持:str 和 datetime")


book = Book(publish_date=12)
print(book)


def conver_to_datetime(user_input) -> datetime:
    if isinstance(user_input, str):
        return datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
    elif isinstance(user_input, datetime):
        return user_input
    raise TypeError("不支持的参数类型，仅支持:str 和 datetime")


@attr.s
class NoteBook:
    publish_date: datetime = attr.ib(default=None, converter=conver_to_datetime)


notebook = NoteBook(publish_date='2021-09-13 00:00:00')
print(notebook)
