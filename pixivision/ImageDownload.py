# -*- coding: utf-8 -*-
import os
import threading

from pixiv_config import IMAGE_SVAE_BASEPATH, USE_FILTER, REDIS_IP, REDIS_PORT, IMAGE_USE_ORG_NAME
from pixivapi.PixivApi import PixivApi
from pixivision.PixivisionDownloader import HtmlDownloader
from utils import CommonUtils
from utils.LoggerUtil import error_log


# redis filter 过滤装饰器 过滤已下载过的链接
# 使用redis会使整个项目变得太重。废弃不用。
# def redisFilterDecp(r=None):
#     def _deco(func):
#         def new_fun(cls, url, save_path, quality):
#             if USE_FILTER:
#                 from utils.RedisFilter import RedisFilter
#                 redis_filter = RedisFilter(r, block_num=BLOCK_NUM, filter_key=REDIS_FILTER_KEY)
#                 if not redis_filter.is_contained(url):
#                     rt = func(cls, url, save_path, quality)
#                     redis_filter.add(url)
#                     print("Redis Filter Add url success: " + url)
#                     return rt
#                 else:
#                     print("The URL has been filtered: " + url)
#             else:
#                 return func(cls, url, save_path, quality)
#
#         return new_fun
#
#     return _deco


class ImageDownload(object):
    # # redis 连接只需要一个，在类中共享
    # if USE_FILTER:
    #     import redis
    #     r = redis.Redis(REDIS_IP, REDIS_PORT)
    # else:
    #     r = None

    @classmethod
    def get_pixivision_topics(cls, url, path):
        topic_list = HtmlDownloader.parse_illustration_topic(HtmlDownloader.download(url))
        if not topic_list:
            error_log(url + " not find any illustration topic")
            return
        for topic in topic_list:
            try:
                # 需要过滤掉特殊字符，否则会创建文件夹失败。
                # 创建特辑文件夹，写入特辑信息。
                save_path = path + "/" + CommonUtils.filter_dir_name(topic.title)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                CommonUtils.write_topic(save_path + "/topic.txt", topic)
                topic['save_path'] = save_path
            except Exception, e:
                continue
                error_log("Create topic path fail,topic url:" + topic.Href)
                error_log(e)
        return topic_list

    @classmethod
    def download_topics(cls, url, path, quality=1, create_path=False):
        html = HtmlDownloader.download(url)
        illu_list = HtmlDownloader.parse_illustration(html)
        title_des = HtmlDownloader.get_title(html)
        # # 是否由该线程自主创建文件夹
        if create_path and title_des and title_des.has_key('title'):
            path = path + "/" + title_des['title']
            os.makedirs(path)
        if title_des and illu_list:
            title_des["size"] = len(illu_list)
            CommonUtils.write_topic_des(path + "/topic.txt", title_des)
        if not illu_list:
            return
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
                        if IMAGE_USE_ORG_NAME:
                            save_path = path + "/p_%s_%s%s" % (id, filename, extension)
                        else:
                            save_path = path + "/p_%s%s" % (id, extension)
                        print(save_path)
                        PixivApi.download(download_url, path=save_path)
                    else:
                        print(illu.title + " can't get detail id :" + id)
                else:
                    # 直接下载 pixivision 展示图
                    print(path + "/p_%s_%s%s" % (id, filename, extension))
                    PixivApi.download(illu.image, path=path + "/p_%s_%s%s" % (id, filename, extension))
            except Exception, e:
                error_log("Download Illu Fail:" + " Illustration :" + str(illu))
                error_log(e)
                continue
        print '*' * 10
        print url + " Download End!"

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

    @classmethod
    def download_image_byid(cls, id, prefix=None):
        if id:
            detail = PixivApi.illust_detail(id)
            print(detail)
            if detail:
                download_url = ImageDownload.get_image_url(None, detail)
                if download_url:
                    PixivApi.download(download_url, prefix=prefix)
                else:
                    print("download by id fail,can't find download url")
            else:
                print("can't get detail id:" + str(id))

    @classmethod
    def download_byurl(cls, url, prefix=None):
        illust_id = CommonUtils.get_url_param(url, "illust_id")
        if illust_id:
            ImageDownload.download_image_byid(illust_id, prefix=prefix)
        else:
            PixivApi.download(url.strip(), prefix=prefix)


class IlluDownloadThread(threading.Thread):
    def __init__(self, url, path=IMAGE_SVAE_BASEPATH, quality=1, create_path=False):
        threading.Thread.__init__(self, name="Download-" + url)
        self.url = url
        self.path = path
        self.quality = quality
        self.create_path = create_path

    def run(self):
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except Exception, e:
                error_log("make dir Fail:" + self.path)
                error_log(e)
                return
        ImageDownload.download_topics(self.url, self.path, quality=self.quality, create_path=self.create_path)
