# -*- coding: utf-8 -*-
import re

import pixiv_config
from pixivsion.ImageDownload import IlluDownloadThread
from pixivsion.PixivisionLauncher import PixivisionLauncher


def set_int(intNum):
    try:
        return int(intNum)
    except:
        print("无法解析页码，默认下载第一页")
        return 1


if __name__ == '__main__':
    print("这里是Pixivsion插画特辑下载器。")
    print("如果遇见什么问题或发现BUG，请联系我Github:(https://github.com/imn5100)或Email:(imn5100_chu2@163.com)。")
    download_type = input(
            "请选择你需要下载的类型：\n输入1.特辑列表页(多组特辑)输入页码即可\n输入2.需要下载的特辑页 \n")
    if download_type == 1:
        page_index = raw_input("请输入需要下载的页面页码,如果是不存在页码将下载失败\n")
        page_index = set_int(page_index)
        url = pixiv_config.LINK_URL % page_index
        PixivisionLauncher(url, save_path=pixiv_config.IMAGE_SVAE_BASEPATH, quality=pixiv_config.IMAGE_QUALITY).start()
    else:
        while True:
            url = raw_input('请输入需要下载的连接:\n')
            if re.match("http://www.pixivision.net/(zh|ja|en)/a/\d*", url.strip()):
                break
            else:
                print ("输入连接不支持，请输入Pixivsion 站特辑网址")
                continue
        IlluDownloadThread(url.strip(), path=pixiv_config.IMAGE_SVAE_BASEPATH,
                           quality=pixiv_config.IMAGE_QUALITY).start()
