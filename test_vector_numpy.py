import time

import numpy as np
import pandas as pd

# 寻找数字的总和
# 循环 耗时  0.13863015174865723 seconds
start = time.time()
# 遍历之和
total = 0
# 遍历150万个数字
for item in range(0, 1500000):
    total = total + item

str(total)
end = time.time()
print("循环")
print(str(end - start) + " seconds")

start = time.time()

# 向量化和--使用numpy进行向量化   耗时 0.0030205249786376953 seconds
# np.range创建从0到1499999的数字序列
np.sum(np.arange(1500000))

end = time.time()
print("pandas向量")
print("耗时 " + str(end - start) + " seconds")

# DataFrame 数学运算
# 循环
df = pd.DataFrame(np.random.randint(1, 50,
                                    size=(5000000, 4)),
                  columns=('a', 'b', 'c', 'd'))

# 超时了
# for idx, row in df.iterrows():
#     # creating a new column
#     df.at[idx, 'ratio'] = 100 * (row["d"] / row["c"])
# end = time.time()
# print(end - start)

# pandas向量 耗时 0.14327335357666016 seconds
start = time.time()
df['e'] = df['b'] + df['c']
df.loc[df['a'] <= 25, 'e'] = df['b'] - df['c']
df.loc[df['a'] == 0, 'e'] = df['d']
end = time.time()
print("pandas向量")
print("耗时 " + str(end - start) + " seconds")

m = np.random.rand(1, 5)
x = np.random.rand(5000000, 5)

# DataFrame循环 耗时 13.203125 seconds
print("DataFrame循环")
total = 0
tic = time.process_time()

for i in range(0, 5000000):
    for j in range(0, 5):
        total = total + x[i][j] * m[0][j]

toc = time.process_time()
print("耗时 " + str((toc - tic)) + " seconds")

# DataFrame向量 0.375seconds

print("DataFrame向量")
tic = time.process_time()
np.dot(x, m.T)

toc = time.process_time()
print("耗时 " + str((toc - tic)) + "seconds")
