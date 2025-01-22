# 共享缓存处理数据
import time
from multiprocessing.shared_memory import SharedMemory


def is_memory_empty(shm):
    """检查共享内存是否为空（全为 0）"""
    return all(byte == 0 for byte in shm.buf)


def clear_memory(shm):
    """清理共享内存（将所有字节设置为 0）"""
    shm.buf[:] = b'\x00' * len(shm.buf)


def process_cache():
    # 连接到共享内存
    shm = SharedMemory(name="my_shared_memory")
    while True:
        if not is_memory_empty(shm):
            data = bytes(shm.buf).rstrip(b'\x00').decode('utf-8')
            # 读取缓存中的最新数据
            print(f"处理进程：读取到数据 -> {data}")
            # 模拟数据处理逻辑
            try:
                # 这里可以替换为实际的数据处理逻辑
                print(f"处理进程：正在处理数据 -> {data}")
                time.sleep(3)  # 模拟处理耗时
                print(f"处理进程：数据处理成功 -> {data}")
                clear_memory(shm)
            except Exception as e:
                print(f"处理进程：数据处理失败 -> {e}")
                # 如果处理失败，可以将数据重新放回缓存
        else:
            time.sleep(4)
    shm.close()


if __name__ == "__main__":
    # 使用 multiprocessing.Manager 创建共享的本地缓存
    process_cache()
