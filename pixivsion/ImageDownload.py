# -*- coding: utf-8 -*-
import os
import threading

from pixiv_config import IMAGE_QUALITY
from pixivapi.PixivApi import PixivApi
from pixivsion.PixivsionDownloader import HtmlDownloader
from utils import CommonUtils


class ImageDownload(object):
    @classmethod
    def get_pixivsion_topics(cls, url, path):
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
    def download_topics(cls, url, path, quality=2):
        illu_list = HtmlDownloader.parse_illustration(HtmlDownloader.download(url))
        for illu in illu_list:
            filename = CommonUtils.filter_dir_name(illu.title)
            extension = os.path.splitext(illu.image)[1]
            id = CommonUtils.get_url_param(illu.image_page, "illust_id")
            if quality == 1:
                # 通过api获取 插画原图地址，下载原图
                detail = PixivApi.illust_detail(id)
                if detail:
                    if detail.illust.page_count > 1:
                        print("Illust Detail has other illust:\n Detail:" + str(detail))
                        print(path + "/p_%s_%s%s" % (id, filename, extension))
                        PixivApi.download(illu.image, path=path + "/p_%s_%s%s" % (id, filename, extension))
                    else:
                        download_url = detail.illust.meta_single_page.original_image_url
                        print(path + "/p_%s_%s%s" % (id, filename, extension))
                        PixivApi.download(download_url, path=path + "/p_%s_%s%s" % (id, filename, extension))
                else:
                    print(illu.title + " can't get detail id :" + id)
            else:
                # 直接下载 pixivsion 展示图
                print(path + "/p_%s_%s%s" % (id, filename, extension))
                PixivApi.download(illu.image, path=path + "/p_%s_%s%s" % (id, filename, extension))


class DownloadThread(threading.Thread):
    def __init__(self, url, path, quality=2):
        threading.Thread.__init__(self, name="Download-" + url)
        self.url = url
        self.path = path
        self.quality = quality

    def run(self):
        ImageDownload.download_topics(self.url, self.path, self.quality)
