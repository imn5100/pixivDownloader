# -*- coding: utf-8 -*-
import os

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
    def download_topics(cls, url, path):
        illu_list = HtmlDownloader.parse_illustration(HtmlDownloader.download(url))
        for illu in illu_list:
            filename = illu.title
            extension = os.path.splitext(illu.image)[1]
            id = CommonUtils.get_url_param(illu.image_page, "illust_id")
            if IMAGE_QUALITY == 1:
                # 通过api获取 插画原图地址，下载原图
                detail = PixivApi.illust_detail(id)
                download_url = detail.illust.meta_single_page.original_image_url
                print(path + "/p_%s_%s%s" % (id, filename, extension))
                PixivApi.download(download_url, path + "/p_%s_%s%s" % (id, filename, extension))
            else:
                # 直接下载 pixivsion 展示图
                print(path + "/p_%s_%s%s" % (id, filename, extension))
                PixivApi.download(download_url, path + "/p_%s_%s%s" % (id, filename, extension))
