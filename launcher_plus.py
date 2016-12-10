# -*- coding: utf-8 -*-


from pixiv_config import LINK_URL
from pixivision.PixivisionLauncher import PixivisionLauncher

if __name__ == '__main__':
    # Pixivision全站插图爬取
    # 目前有62页 共61*20+ 5 特辑（2016/12/10 2:44数据）
    urls = [LINK_URL % n for n in range(1, 63)]
    # 步伐，每次启动 4 *20 个进程
    step = 4
    length = len(urls)
    start = 0
    while start < length:
        launchers = []
        for url in urls[start:(start + step)]:
            print("start:" + url)
            launchers.append(PixivisionLauncher(url, "E://imageDownLoad//z_pixivision_download", 1))
        for launcher in launchers:
            launcher.start()
        for launcher in launchers:
            launcher.join()
        start += step
