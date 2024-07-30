import threading
import time


def multi_thread(s, t):
    time.sleep(t)
    print(s)


if __name__ == "__main__":
    m_list = [['c', 2], ['b', 1], ['d', 3], ['a', 4]]
    for i in m_list:
        ts = threading.Thread(target=multi_thread, args=(i))
        ts.start()
