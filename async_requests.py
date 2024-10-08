import asyncio
import concurrent
import time
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import grequests
import httpx
import requests


session = requests.Session()
req_list = [grequests.get('https://www.baidu.com', session=session) for i in range(100)]
start = time.time()
res_list = grequests.map(req_list)
print(f"grequests: {time.time() - start}")


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main_aiohttp():
    url = 'https://www.baidu.com'
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for _ in range(100)]
        responses = await asyncio.gather(*tasks)


start_time = time.time()
asyncio.run(main_aiohttp())
print(f"Aiohttp + asyncio: {(time.time() - start_time)} seconds")


async def main_asyncio():
    url = 'https://www.baidu.com'
    tasks = [asyncio.create_task(asyncio.sleep(0), name=f'Task-{i}') for i in range(100)]  # 创建占位符任务
    for task in tasks:
        asyncio.create_task(fetch_with_aiohttp(task.get_name()), name=task.get_name())  # 替换为实际请求任务


async def fetch_with_aiohttp(task_name):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.baidu.com') as response:
            await response.text()


start_time = time.time()
asyncio.run(main_asyncio())
print(f"Pure asyncio: {(time.time() - start_time)} seconds")


def fetch_with_requests():
    response = session.get('https://www.baidu.com')
    response.raise_for_status()


start_time = time.time()
with ThreadPoolExecutor(max_workers=100) as executor:
    tasks = [executor.submit(fetch_with_requests) for _ in range(100)]
    for future in concurrent.futures.as_completed(tasks):
        pass

print(f"Multithreading: {(time.time() - start_time)} seconds")


async def fetch(session, url):
    response = await session.get(url)
    return await response.aread()


async def httpx_main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, 'https://www.baidu.com') for _ in range(100)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        total_time = end_time - start_time
    return total_time


total_time = asyncio.run(httpx_main())
print(f"httpx time: {total_time:.2f} seconds")

# grequests: 0.45383763313293457
# Aiohttp + asyncio: 0.5920767784118652 seconds
# Aiohttp + uvloop + asyncio 说明：uvloop不支持windows
# Pure asyncio: 0.020534992218017578 seconds
# Multithreading: 0.43889522552490234 seconds
# httpx time: 0.64 seconds
