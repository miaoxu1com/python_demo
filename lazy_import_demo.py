import importlib


# 使用 Importlib 进行延迟加载
def load_module(module_name):
    module = importlib.import_module(module_name)
    return module


my_module = load_module('sys')


# 根据用户输入加载模块
def load_module_by_name(module_name):
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        print(f"Module {module_name} not found.")
        return None


loaded_module = load_module_by_name('sys')

# 使用这种加载方式pycharm无法智能提示
if loaded_module:
    print((loaded_module.path))


# 使用 If 语句进行条件加载
def load_module_conditionally(condition):
    if condition:
        module_name = "sys"  # Replace with the actual module name
        module = importlib.import_module(module_name)
        return module
    else:
        return None


# Check a condition to determine if the module should be loaded
should_load_module = True  # Replace with your actual condition
loaded_module = load_module_conditionally(should_load_module)
