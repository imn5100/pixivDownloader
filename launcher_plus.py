# -*- coding: utf-8 -*-
import threading

from twisted.python.threadpool import ThreadPool

from pixiv_config import LINK_URL
from pixivision.PixivisionLauncher import start

if __name__ == '__main__':
    # Pixivision全站插图爬取
    # 目前有62页 共61*20+ 5 特辑（2016/12/10 2:44数据）
    urls = [LINK_URL % n for n in range(1, 63)]
    # 5*20 最大100线程在运行
    pool = ThreadPool(minthreads=0, maxthreads=5)
    for url in urls:
        pool.callInThread(start, url)
    pool.start()
