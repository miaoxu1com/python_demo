import time
from lxml import etree
import aiohttp
import asyncio
import time

urls = [
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16488',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16583',
    'https://www.baidu.com'
]
htmls = []
titles = []
sem = asyncio.Semaphore(10)  # 信号量，控制协程数，防止爬的过快
'''
提交请求获取AAAI网页html
'''


# 并发异步返回一个处理一个
async def get_html(url, tt):
    # async with是异步上下文管理器
    async with aiohttp.ClientSession() as session:  # 获取session
        async with session.request('GET', url) as resp:  # 提出请求
            html = await resp.read()  # 直接获取到bytes
            htmls.append(html)
            title = etree.HTML(html).xpath('//*[@id="title"]/text()')
            time.sleep(tt)
            print(url)
            titles.append(''.join(title))
