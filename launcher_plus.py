# -*- coding: utf-8 -*-


from pixiv_config import LINK_URL, PAGE_NUM, IMAGE_SVAE_BASEPATH, IMAGE_QUALITY
from pixivision.PixivisionLauncher import PixivisionLauncher

if __name__ == '__main__':
    # Pixivision全站插图爬取
    urls = [LINK_URL % n for n in range(1, PAGE_NUM + 1)]
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
