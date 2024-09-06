# 动态代码 ide识别失败
# 动态生成变量
var_name = "dynamic_var"
var_value = 42
exec(f"{var_name} = {var_value}")
print(dynamic_var)

# 动态生成函数
func_code = """
def dynamic_function(x, y):
    return x + y
"""
exec(func_code)
result = dynamic_function(3, 4)
print(result)

# 动态创建类
class_name = "DynamicClass"
class_code = """
class DynamicClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y
"""

exec(class_code)
instance = DynamicClass(3, 4)
result = instance.add()
print(result)  # 输出 7

# 执行外部文件
# exec 函数还可以用于执行外部文件中的 Python 代码。这对于将代码模块化或从外部源加载代码非常有用。

# file_contents = open("external_code.py").read()
# exec(file_contents)
# 在这个示例中，打开了名为"external_code.py"的外部文件，然后使用exec执行了其中的Python代码。
# 作用域控制
# globals 和 locals 在使用 exec 函数时，可以传递两个字典参数，即 globals 和 locals。这些参数控制了执行代码的作用域。globals
# 参数用于指定全局作用域，而 locals 参数用于指定局部作用域。

global_var = 42
local_var = 10

code = """
result = global_var + local_var
"""

namespace = {"global_var": global_var, "local_var": local_var}
exec(code, namespace)

result = namespace["result"]
print(result)  # 输出 52

# 在这个示例中，使用 globals 和 locals 参数明确指定了变量的作用域。
# exec 内的变量
# 请注意，exec 函数内部创建的变量默认情况下将位于局部作用域。如果要将变量置于全局作用域，你需要在代码中明确声明它们。
global_var = 42

code = """
local_var = 10
"""

namespace = {"global_var": global_var}
exec(code, namespace)


# 这里访问 local_var 会引发 NameError
# 在这个示例中，local_var 变量位于 exec 函数的局部作用域，无法在全局作用域中访问。

# 安全性考虑
# 虽然 exec 函数非常强大，但在使用时需要格外小心，以避免潜在的安全问题。以下是一些安全性考虑：
# 避免用户输入 避免将来自不受信任的来源的用户输入传递给 exec 函数，因为这可能导致代码注入攻击。
# 限制权限 在执行动态代码之前，考虑将权限限制在必要的最小程度上，以防止潜在的不安全操作。
# 最佳实践 在使用 exec 函数时，请遵循以下最佳实践：
#
# 仅在必要时使用 exec，尽量避免使用它。
# 避免接受来自不受信任源的用户输入。
# 明确指定 globals 和 locals 参数，以更好地控制作用域。
# 总结
# Python 中的 exec 函数允许你运行时执行动态生成的 Python 代码，提供了强大的灵活性，但也需要小心使用以确保安全性。
# 本文介绍了 exec 函数的高级用法，包括动态代码生成、执行外部文件、作用域控制和安全性考虑。希望这些示例和最佳实践有助于你更好地理解和使用 exec 函数。
#
# 在 Python 中，eval() 和 exec() 都可以用于动态执行代码，但它们的具体用途和行为略有不同：
# eval() 函数主要用于计算数学表达式或解析字符串中的表达式。它将字符串作为参数，将其作为一个 Python 表达式进行求值并返回结果。
# eval() 函数可以接受一个字典作为可选参数，用于指定全局和局部命名空间。
# exec()函数则用于执行一段代码块，可以是单个语句或多个语句。
# 与 eval() 不同，exec() 不会返回任何值，它只是执行代码并将结果存储在变量中（如果指定了变量）。exec() 函数也可以接受一个字典作为可选参数，用于指定全局和局部命名空间。
# 因此，eval() 和 exec() 的主要区别在于它们的返回值。eval() 返回表达式的计算结果，而 exec() 没有返回值，只是在运行时执行代码。
# 此外，eval() 更适合用于简单的表达式计算，而 exec() 更适合用于复杂的代码块执行。但同时这两个函数都存在安全风险，使用的时候请谨慎。


# 动态添加实例方法
class Person(object):
    country = 'china'

    def __init__(self, name):
        self.name = name


@classmethod
def run(cls):
    print('%s在奔跑' % cls.country)


Person.run = run
Person.run()

delattr(Person, "run")


# 动态添加类方法：
# 添加类方法，是把这个方法添加给类。因此添加类方法的时候不是给对象添加，而是给类添加。
@staticmethod
def run():
    print('在奔跑')


Person.run = run
Person.run()

# 动态删除属性和方法
del Person.run

# attrs 库 装饰器设置类

# os.path 动态获取路径 os.path.normcase
