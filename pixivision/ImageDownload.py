# -*- coding: utf-8 -*-
import os
import threading

from pixiv_config import IMAGE_SVAE_BASEPATH
from pixivapi.PixivApi import PixivApi
from pixivision.PixivisionDownloader import HtmlDownloader
from utils import CommonUtils


class ImageDownload(object):
    @classmethod
    def get_pixivision_topics(cls, url, path):
        topic_list = HtmlDownloader.parse_illustration_topic(HtmlDownloader.download(url))
        for topic in topic_list:
            # 创建特辑文件夹，写入特辑信息。
            # 需要过滤掉特殊字符，否则会创建文件夹失败。
            save_path = path + "/" + CommonUtils.filter_dir_name(topic.title)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            CommonUtils.write_topic(save_path + "/topic.txt", topic)
            topic['save_path'] = save_path
        return topic_list

    @classmethod
    def download_topics(cls, url, path, quality=1):
        illu_list = HtmlDownloader.parse_illustration(HtmlDownloader.download(url))
        for illu in illu_list:
            try:
                filename = CommonUtils.filter_dir_name(illu.title)
                extension = os.path.splitext(illu.image)[1]
                id = CommonUtils.get_url_param(illu.image_page, "illust_id")
                if quality == 1:
                    # 通过api获取 插画原图地址，下载原图
                    detail = PixivApi.illust_detail(id)
                    if detail:
                        download_url = ImageDownload.get_image_url(illu, detail)
                        print(path + "/p_%s_%s%s" % (id, filename, extension))
                        PixivApi.download(download_url, path=path + "/p_%s_%s%s" % (id, filename, extension))
                    else:
                        print(illu.title + " can't get detail id :" + id)
                else:
                    # 直接下载 pixivision 展示图
                    print(path + "/p_%s_%s%s" % (id, filename, extension))
                    PixivApi.download(illu.image, path=path + "/p_%s_%s%s" % (id, filename, extension))
            except Exception, e:
                print("Download Illu Fail:" + e + " Illustration :" + str(illu))
                continue

    @classmethod
    def get_image_url(cls, illu, detail):
        # page_count>1 说明id对应多组插画（即插画集）。无法获得原图地址，下载大图
        show_msg = ["original image", "large image", "normal image"]
        flag = 0
        if detail.illust.page_count > 1:
            try:
                download_url = detail.illust.image_urls.large
                flag = 1
            except:
                download_url = illu.image
                flag = 2
        else:
            try:
                download_url = detail.illust.meta_single_page.original_image_url
            except:
                try:
                    # 获取原图失败 获取大图
                    download_url = detail.illust.image_urls.large
                    flag = 1
                except:
                    # 获取大图失败，直接使用展示图
                    download_url = illu.image
                    flag = 2
        print("Download " + show_msg[flag])
        return download_url


class IlluDownloadThread(threading.Thread):
    def __init__(self, url, path=IMAGE_SVAE_BASEPATH, quality=1):
        threading.Thread.__init__(self, name="Download-" + url)
        self.url = url
        self.path = path
        self.quality = quality

    def run(self):
        ImageDownload.download_topics(self.url, self.path, self.quality)
