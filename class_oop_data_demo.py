# @property 是 python 的一个内置装饰器，使用装饰器的目的是改变类的方法或者属性，这样调用者就无需在代码中做任何改动
# 上面的代码清晰地展示了如何用 pythonic 的方式使用 @property 装饰器实现 setter 和 getter 属性。同时实现了对属性赋值时的有效性检查
class Adult(object):
    def __init__(self):
        self.__age = 0

    @property
    def age(self):
        print('getter() method called')
        return self.__age

    @age.setter
    def age(self, value):
        if value < 18:
            raise ValueError('Sorry, you are a child, games not allowed')
        print('setter() method called')
        self.__age = value


xiaoli = Adult()
xiaoli.age
xiaoli.age = 19
