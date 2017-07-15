# -*- coding: utf-8 -*-
import os
import threading

from pixiv import PixivImageDownloader
from pixiv_config import IMAGE_SAVE_BASEPATH, IMAGE_USE_ORG_NAME
from pixivapi.PixivApi import PixivApi
from pixivision.PixivisionDownloader import HtmlDownloader
from utils import CommonUtils
from utils.LoggerUtil import error_log


class ImageDownload(object):
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
            except Exception as e:
                error_log("Create topic path fail,topic url:" + topic.Href)
                error_log(e)
                continue
        return topic_list

    @classmethod
    def download_topics(cls, url, path, create_path=False):
        html = HtmlDownloader.download(url)
        illu_list = HtmlDownloader.parse_illustration(html)
        title_des = HtmlDownloader.get_title(html)
        # # 是否由该线程自主创建文件夹
        if create_path and title_des and title_des.has_key('title'):
            path = path + "/" + title_des['title']
            if not os.path.exists(path):
                os.makedirs(path)
        if title_des and illu_list:
            title_des["size"] = len(illu_list)
            title_des["url"] = url
            CommonUtils.write_topic_des(path + "/topic.txt", title_des)
        if not illu_list:
            return
        for illu in illu_list:
            id = CommonUtils.get_url_param(illu.image_page, "illust_id")
            PixivImageDownloader.download_all_by_id(id, path + '/', limit_p=False)
        print '*' * 10
        print url + " Download End!"
        return path

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
            if detail:
                download_url = ImageDownload.get_image_url(None, detail)
                if download_url:
                    return PixivApi.download(download_url, prefix=prefix)
                else:
                    print("error", "download by id fail,can't find download url")
            else:
                print("error", "can't get detail id:" + str(id))

    @classmethod
    def download_byurl(cls, url, prefix=None):
        illust_id = CommonUtils.get_url_param(url, "illust_id")
        if illust_id:
            return ImageDownload.download_image_byid(illust_id, prefix=prefix)
        else:
            return PixivApi.download(url.strip(), prefix=prefix)


class IlluDownloadThread(threading.Thread):
    def __init__(self, url, path=IMAGE_SAVE_BASEPATH, create_path=False):
        threading.Thread.__init__(self, name="Download-" + url)
        self.url = url
        self.path = path
        self.create_path = create_path
        self.success = None
        self.fail = None

    def run(self):
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except Exception, e:
                error_log("make dir Fail:" + self.path)
                error_log(e)
                return
        try:
            path = ImageDownload.download_topics(self.url, self.path,
                                                 create_path=self.create_path)
            if self.success:
                self.success(CommonUtils.build_callback_msg(path, url=self.url))
        except Exception as e:
            print e
            if self.fail:
                self.fail()

    def register_hook(self, success_callback=None, fail_callback=None):
        if success_callback:
            self.success = success_callback
        if fail_callback:
            self.fail = fail_callback
        return self
