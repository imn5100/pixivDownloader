# -*- coding: utf-8 -*-

import time

from pixiv_config import LINK_URL, PAGE_NUM, IMAGE_SVAE_BASEPATH, IMAGE_QUALITY
from pixivision.PixivisionLauncher import PixivisionLauncher
from utils.LoggerUtil import error_log

if __name__ == '__main__':
    error_log("start" + str(time.time()))
    # Pixivision全站插图爬取
    urls = [LINK_URL % n for n in range(10, PAGE_NUM + 1)]
    # 步伐，每次启动 2 *20 个图片下载进程 ，可根据电脑性能调整线程大小。其实运行速度和内存CPU关系不大，关键是网速
    step = 2
    length = len(urls)
    start = 0
    while start < length:
        launchers = []
        for url in urls[start:(start + step)]:
            print("Start " + url)
            launchers.append(PixivisionLauncher(url, IMAGE_SVAE_BASEPATH, IMAGE_QUALITY))
        for launcher in launchers:
            launcher.start()
        for launcher in launchers:
            launcher.join()
        start += step
    error_log("end" + str(time.time()))
