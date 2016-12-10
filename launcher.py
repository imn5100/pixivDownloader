# -*- coding: utf-8 -*-
import re

import pixiv_config
from pixivision.ImageDownload import IlluDownloadThread, ImageDownload
from pixivision.PixivisionLauncher import PixivisionLauncher


def set_int(intNum):
    try:
        return int(intNum)
    except:
        return 0


def main_for_zh():
    print("这里是Pixivision插画特辑下载器。")
    print("如果遇见什么问题或发现BUG，请联系我Github:(https://github.com/imn5100)或Email:(imn5100_chu2@163.com)。")
    download_type = raw_input(
            "请选择你需要下载的类型：\n输入1.特辑列表页(多组特辑)输入页码即可\n输入2.下载特辑页\n输入3.直接使用图片url下载（部分下载失败的图片可直接使用此功能下载）\n输入4.通过P站id下载\n输入其他数字.退出\n")
    download_type = set_int(download_type)
    if download_type == 0:
        exit()
    if download_type == 1:
        page_index = raw_input("请输入需要下载的页面页码,如果是不存在页码将下载失败\n")
        page_index = set_int(page_index)
        if page_index == 0:
            page_index = 1
        url = pixiv_config.LINK_URL % page_index
        print("充能ing...")
        PixivisionLauncher(url, save_path=pixiv_config.IMAGE_SVAE_BASEPATH, quality=pixiv_config.IMAGE_QUALITY).start()
    elif download_type == 2:
        while True:
            url = raw_input('请输入需要下载的链接:\n')
            if re.match("http://www.pixivision.net/(zh|ja|en|zh-tw)/a/\d*", url.strip()):
                break
            else:
                print ("输入连接不支持，请输入Pixivision 站特辑网址。栗子:http://www.pixivision.net/zh/a/1906 ")
                continue
        save_path = raw_input("请输入有效存储路径：\n")
        print("充能ing...")
        IlluDownloadThread(url.strip(), path=save_path.decode("utf-8"), quality=pixiv_config.IMAGE_QUALITY).start()
    elif download_type == 3:
        url = str(raw_input("请输入Pixiv图片url:")).strip()
        ImageDownload.download_byurl(url)
    elif download_type == 4:
        id = int(raw_input("请输入Pixiv插画ID:"))
        ImageDownload.download_image_byid(id)
    else:
        print("退出!")
        return


def main_for_en():
    print("Here is the Pixivision illustrator downloader.")
    print(
        "If you have any problems or find bugs, please contact me at github: (https://github.com/imn5100) or Email: (imn5100_chu2@163.com).")
    download_type = raw_input(
            "Please select the type you want to download: \n Enter 1. The special list page (groups of specials) enter the page number to \n "
            "Enter 2. Download the special page \n "
            "Enter 3.Use the image url to download (some download failed pictures Direct use of this feature to download) \n"
            " Enter 4. Through the P station id download \n Enter the other numbers.\n")
    download_type = set_int(download_type)
    if download_type == 0:
        exit()
    if download_type == 1:
        page_index = raw_input(
                "Please enter the page number to be downloaded. If the page number does not exist, the download will fail\n")
        page_index = set_int(page_index)
        if page_index == 0:
            page_index = 1
        url = pixiv_config.LINK_URL % page_index
        print("Charging...")
        PixivisionLauncher(url, save_path=pixiv_config.IMAGE_SVAE_BASEPATH, quality=pixiv_config.IMAGE_QUALITY).start()
    elif download_type == 2:
        while True:
            url = raw_input('Please enter a Pixivision URL to download:\n')
            if re.match("http://www.pixivision.net/(zh|ja|en|zh-tw)/a/\d*", url.strip()):
                break
            else:
                print (
                    "The input URL is not supported, enter the Pixivision Station URL,Example:http://www.pixivision.net/en/a/1906 ")
                continue
        save_path = raw_input("Please enter a valid storage path:\n")
        print("Charging...")
        IlluDownloadThread(url.strip(), path=save_path.decode("utf-8"), quality=pixiv_config.IMAGE_QUALITY).start()
    elif download_type == 3:
        url = str(raw_input("Please enter the Pixiv image url:")).strip()
        ImageDownload.download_byurl(url)
        print("Charging...")
    elif download_type == 4:
        id = int(raw_input("Please enter a Pixiv illustration ID:"))
        ImageDownload.download_image_byid(id)
    else:
        print("Exit!")
        return


if __name__ == '__main__':
    language = raw_input("选择语言(Choose A Language):\n(输入 1)中文\n(Enter 2)English\n")
    language = set_int(language)
    if language == 0:
        exit()
    if language == 1:
        main_for_zh()
    else:
        main_for_en()
