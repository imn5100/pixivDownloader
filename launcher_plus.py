# -*- coding: utf-8 -*-
import time

from pixiv_config import LINK_URL, PAGE_NUM, IMAGE_SVAE_BASEPATH, IMAGE_QUALITY
from pixivision.PixivisionLauncher import PixivisionLauncher, start
from utils.LoggerUtil import error_log


# 使用线程池，不需要等线程*全部*顺序执行完毕再开启下个线程
def run_by_pool():
    # 9:49     # 14:15
    # Pixivision全站插图爬取
    from twisted.python.threadpool import ThreadPool
    urls = [LINK_URL % n for n in range(PAGE_NUM, 2)]
    # 5*20 最大100线程在运行
    error_log("start：" + str(time.time()))
    pool = ThreadPool(minthreads=1, maxthreads=5)
    for url in urls:
        pool.callInThread(start, url, save_path=IMAGE_SVAE_BASEPATH, quality=IMAGE_QUALITY)
    pool.start()
    while True:
        # 每20s判断一次线程池状态，没有线程正在运行则停止下载进程
        time.sleep(20)
        if len(pool.working) == 0:
            pool.stop()
            error_log("end：" + str(time.time()))
            break


# 没有安装 twisted 时，只能使用 顺序线程下载。
def run_by_list():
    error_log("start：" + str(time.time()))
    # Pixivision全站插图爬取
    urls = [LINK_URL % n for n in range(1, PAGE_NUM + 1)]
    # 步伐，每次启动 2 *20 个图片下载进程 ，可根据电脑性能调整线程大小。其实运行速度和内存CPU关系不大，关键是网速
    step = 2
    length = len(urls)
    start_index = 0
    while start_index < length:
        launchers = []
        for url in urls[start_index:(start_index + step)]:
            print("Start " + url)
            launchers.append(PixivisionLauncher(url, IMAGE_SVAE_BASEPATH, IMAGE_QUALITY))
        for launcher in launchers:
            launcher.start()
        for launcher in launchers:
            launcher.join()
        start_index += step
    error_log("end：" + str(time.time()))


if __name__ == '__main__':
    run_by_pool()
