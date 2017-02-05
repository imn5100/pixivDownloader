# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# 为保证访问文件夹编码正常，使用全局的 unicode 编码
import os
import re

from pixiv_config import IMAGE_SVAE_BASEPATH
from pixivision.ImageDownload import IlluDownloadThread


def check_image(dir):
    if os.path.exists(dir):
        # windows系统获取的文件夹名称为GBK编码
        image_fls = os.listdir(dir)
        for image_fl in image_fls:
            # 文件夹名称 widnows获取为gbk，liunx如果默认编码为utf-8则不需要这一步
            image_fl = image_fl
            # 检查是否有特辑描述文件
            base_path = dir + "/" + image_fl
            if os.path.exists(base_path + "/topic.txt"):
                check_num(base_path)
            else:
                print("Not found topic.txt.\tPath：" + base_path.encode("utf-8"))


# 检查是否下载完全
def check_num(base_path):
    true_image_num = len(os.listdir(base_path))
    content = open(base_path + "/topic.txt", "r").read()
    res = re.search("IlluNum = \d*", content)
    if res:
        # 获取专题插画文件数量。
        image_num = re.search("IlluNum = \d*", content).group().split(" ")[-1]
        if int(true_image_num) - int(image_num) >= 1:
            print("All illustrations have been downloaded.\tPath:" + base_path)
        else:
            # 判断未下载完全时，获取专题url 重新补全下载
            print(base_path + " " + str(int(true_image_num) - 1) + "/" + image_num)
            completion(base_path, content)
    else:
        print("Not found IlluNum.\tPath:" + base_path + "/topic.txt")
        completion(base_path, content)


# 获取topic文件中的href ，补全下载
def completion(base_path, content):
    href_str = re.search(r"Href = [a-zA-z]+://[^\s]*", content).group()
    if href_str:
        href = re.search(r"Href = [a-zA-z]+://[^\s]*", content).group().split(" ")[-1]
        print("start:" + href)
        IlluDownloadThread(href.strip(), path=base_path).start()
    else:
        print(base_path + " not find topic url")


if __name__ == '__main__':
    # 运行补全检查 前请保证下载时和检查时的命名规范相同，否则会下载两次同样的插画 不同的命名
    check_image(IMAGE_SVAE_BASEPATH)
