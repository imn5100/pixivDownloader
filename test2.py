# -*- coding: utf-8 -*-
import re

from concurrent.futures import ThreadPoolExecutor

from utils.Config import Config
import time


def return_future_result(message):
    time.sleep(2)
    return message


def test_executor():
    pool = ThreadPoolExecutor(max_workers=2)  # 创建一个最大可容纳2个task的线程池
    future1 = pool.submit(return_future_result, ("hello"))  # 往线程池里面加入一个task
    future2 = pool.submit(return_future_result, ("world"))  # 往线程池里面加入一个task
    print(future1.done())  # 判断task1是否结束
    time.sleep(3)
    print(future2.done())  # 判断task2是否结束
    print(future1.result())  # 查看task1返回的结果
    print(future2.result())  # 查看task2返回的结果


def testConfig():
    config = Config('../config.ini', "pixiv")
    print config.get("SEARCH_KEYWORD", "kaka")


def testMatch():
    url = "https://www.pixivision.net/zh/c/illustration/"
    print re.match(r"htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/c/illustration(/|)(\?p=\d+|)", url)


if __name__ == '__main__':
    test_executor()
