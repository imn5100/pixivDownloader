# -*- coding: utf-8 -*-
# 为保证访问文件夹编码正常，使用全局的 unicode 编码
from __future__ import unicode_literals

import os
import re

from pixiv_config import CHECK_IMAGE_VERIFY, IMAGE_SAVE_BASEPATH
from pixivision.PixivisionTopicDownloader import IlluDownloadThread

try:
    from PIL import Image

    can_verify = True
except Exception:
    can_verify = False


# 检查文件是否下载完全
def verify_image(file_path):
    if can_verify and CHECK_IMAGE_VERIFY:
        if not os.path.exists(file_path):
            return False
        try:
            im = Image.open(file_path)
            im.verify()
            return True
        except Exception as e:
            os.remove(file_path)
            print (file_path + "is Broken image File :" + e.message)
            return False
        finally:
            if im:
                im.close()
    else:
        return True


def verify_path(path):
    verify_status = True
    for root, dirs, files in os.walk(path):
        for name in files:
            filename = os.path.join(root, name)
            if filename[-4:].lower() in ('.jpg', '.png', '.gif'):
                if not verify_image(filename):
                    verify_status = False
    return verify_status


def check_image(dir):
    dir = dir.strip()
    if os.path.exists(dir):
        image_fls = os.listdir(dir)
        print ('Dir Count:' + str(len(image_fls)))
        for image_fl in image_fls:
            image_fl = image_fl
            # 检查是否有特辑描述文件
            base_path = dir + "/" + image_fl
            if os.path.isdir(base_path):
                if os.path.exists(base_path + "/topic.txt"):
                    check_num(base_path)
                else:
                    print("Not found topic.txt.\tPath：" + base_path)


# 检查是否下载完全
def check_num(base_path):
    files = os.listdir(base_path)
    true_image_num = len(files)
    if '.DS_Store' in files:
        true_image_num = true_image_num - 1
    content = open(base_path + "/topic.txt", "r").read()
    res = re.search("IlluNum = \d*", content)
    if res:
        # 获取专题插画文件数量。
        image_num = re.search("IlluNum = \d*", content).group().split(" ")[-1]
        if int(true_image_num) - int(image_num) >= 1:
            if verify_path(base_path):
                print("All illustrations have been downloaded.\tPath:" + base_path + " " + str(
                    int(true_image_num) - 1) + "/" + image_num)
            else:
                completion(base_path, content)
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
        IlluDownloadThread(href.strip(), path=base_path, downloader=None).start()
    else:
        print(base_path + " not find topic url")


if __name__ == '__main__':
    check_image(IMAGE_SAVE_BASEPATH)
