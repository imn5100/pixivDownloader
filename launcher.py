# -*- coding: utf-8 -*-
import os
import re

import pixiv_config
from pixivapi.PixivApi import PixivApi
from pixivision.ImageDownload import IlluDownloadThread, ImageDownload
from pixivision.PixivisionLauncher import PixivisionLauncher
from utils import CommonUtils


def set_int(intNum):
    try:
        return int(intNum)
    except:
        print("无法解析页码，默认下载第一页")
        return 1


if __name__ == '__main__':
    print("这里是Pixivision插画特辑下载器。")
    print("如果遇见什么问题或发现BUG，请联系我Github:(https://github.com/imn5100)或Email:(imn5100_chu2@163.com)。")
    download_type = int(raw_input(
            "请选择你需要下载的类型：\n输入1.特辑列表页(多组特辑)输入页码即可\n输入2.需要下载的特辑页\n输入3.直接使用图片url下载（部分下载失败的图片可直接使用此功能下载）\n输入4.通过P站id下载\n"))
    if download_type == 1:
        page_index = raw_input("请输入需要下载的页面页码,如果是不存在页码将下载失败\n")
        page_index = set_int(page_index)
        url = pixiv_config.LINK_URL % page_index
        print("充能ing...")
        PixivisionLauncher(url, save_path=pixiv_config.IMAGE_SVAE_BASEPATH, quality=pixiv_config.IMAGE_QUALITY).start()
    elif download_type == 2:
        while True:
            url = raw_input('请输入需要下载的连接:\n')
            if re.match("http://www.pixivision.net/(zh|ja|en|zh-tw)/a/\d*", url.strip()):
                break
            else:
                print ("输入连接不支持，请输入Pixivision 站特辑网址")
                continue
        print("充能ing...")
        IlluDownloadThread(url.strip(), path=pixiv_config.IMAGE_SVAE_BASEPATH,
                           quality=pixiv_config.IMAGE_QUALITY).start()
    elif download_type == 3:
        url = str(raw_input("请输入Pixiv图片url:")).strip()
        ImageDownload.download_byurl(url)
        print("下载完成")
    elif download_type == 4:
        id = int(raw_input("请输入Pixiv插画ID:"))
        ImageDownload.download_image_byid(id)
        print("下载完成")
