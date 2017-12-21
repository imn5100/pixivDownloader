# -*- coding: utf-8 -*-
import re
import threading

import requests

from pixiv import PixivDataDownloader
from pixiv_config import PIXIV_COOKIES
from utils.AtomicInteger import AtomicInteger
from utils.Config import Config
import time
from PIL import Image


def return_future_result(message):
    time.sleep(2)
    return message


def test_executor():
    pool = ProcessPoolExecutor()  # machine has processors
    future1 = pool.submit(return_future_result, 'hello')  # 往线程池里面加入一个task
    future2 = pool.submit(return_future_result, "world")  # 往线程池里面加入一个task
    future3 = pool.submit(return_future_result, "test")  # 往线程池里面加入一个task
    print(future1.done())  # 判断task1是否结束
    time.sleep(3)
    print(future2.done())  # 判断task2是否结束
    print(future1.result())  # 查看task1返回的结果
    print(future2.result())  # 查看task2返回的结果
    print(future3.result())  # 查看task3返回的结果


def testConfig():
    config = Config('../config.ini', "pixiv")
    print (config.get("SEARCH_KEYWORD", "kaka"))


def testMatch():
    url = "https://www.pixivision.net/zh/c/illustration/"
    print (re.match(r"htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/c/illustration(/|)(\?p=\d+|)", url))


def testImage(file):
    # im = Image.open("/Users/imn5100/Downloads/p_51695014.jpg")
    print (file[-4:].lower())
    print (file[-4:].lower() in ('.jpg', '.png', '.gif'))
    print (time.time())
    im2 = Image.open(file)
    try:
        im2.verify()
    except Exception as e:
        print (e)
    print (time.time())


def testWalk(path):
    import os
    count = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            count = count + 1
            print(os.path.join(root, name))
            # for name in dirs:
            #     print(os.path.join(root, name))
    print (count)


def test_search():
    # print  PixivDataDownloader.search_nologin(u"2000users入り")
    search_handler = PixivDataDownloader.PixivDataHandler(cookies=PIXIV_COOKIES)
    search_handler.check_login_success()


global_num = AtomicInteger()  # 0


def thread_cal():
    global global_num
    for i in xrange(10000):
        global_num.getAndInc()


def test_atomic_int2():
    # Get 10 threads, run them and wait them all finished.
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=thread_cal))
        threads[i].start()
    for i in range(10):
        threads[i].join()
    # Value of global variable can be confused.
    print (global_num == 100000)


def test_proxy():
    proxies = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
    session = requests.session()
    session.proxies = proxies
    r = session.get('https://www.google.com/', proxies=proxies)
    print (r.text)


if __name__ == '__main__':
    # test_atomic_int2()
    test_proxy()
