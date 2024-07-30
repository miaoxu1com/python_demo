import csv
import threading
import pandas as pd


# 写入CSV文件
def write_to_csv(file_name, data):
    with open(file_name, mode='w', newline='') as file:
        fieldnames = ['csv表头']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def start_task(thread_write_csv):
    # 创建线程
    threads = []
    # 启动线程
    for i in range(5):
        thread = threading.Thread(target=thread_write_csv, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 合并CSV文件
    def merge_csv_files(output_file, input_files):
        all_data = []
        for file in input_files:
            df = pd.read_csv(file)
            all_data.append(df)

        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"All files merged into {output_file}")

    # CSV文件列表
    input_files = [f'thread_{i}.csv' for i in range(5)]
    # 合并文件
    merge_csv_files('testdata.csv', input_files)
