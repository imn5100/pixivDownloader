# -*- coding: utf-8 -*-
import re

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

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
    print file[-4:].lower()
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
    print count


if __name__ == '__main__':
    # testImage("/Users/imn5100/Downloads/p_51695014.jpg")
    # testImage("/Users/imn5100/Downloads/p_63414362_4.png")
    # testWalk('/Users/imn5100/Downloads/pixiv/search')
    reader = open('/Users/imn5100/Downloads/pixiv/z_pixivision_download/一生追随！“超凡的反派”特辑/p_10208070.jpg', 'r')
    print reader.read()
    im = Image.open('/Users/imn5100/Downloads/pixiv/z_pixivision_download/一生追随！“超凡的反派”特辑/p_10208070.jpg')
    print im
