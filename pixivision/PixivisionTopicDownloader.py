# -*- coding: utf-8 -*-
import os
import threading

from pixiv import PixivImageDownloader
from pixiv_config import IMAGE_SAVE_BASEPATH
from pixivision.PixivisionHtmlParser import PixivisionHtmlParser
from utils import CommonUtils
from utils.LoggerUtil import error_log


class ImageDownload(object):
    @classmethod
    def get_pixivision_topics(cls, url, path):
        topic_list = PixivisionHtmlParser.parse_illustration_topic(PixivisionHtmlParser.download(url))
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
    def download_topics(cls, url, path, create_path=False, downloader=None):
        html = PixivisionHtmlParser.download(url)
        illu_list = PixivisionHtmlParser.parse_illustration(html)
        title_des = PixivisionHtmlParser.get_title(html)
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
            if downloader:
                downloader.download_all_by_id(id, path + '/')
            else:
                PixivImageDownloader.download_all_by_id(id, path + '/')
        print ('*' * 10)
        print (url + " Download End!")
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
            except Exception:
                download_url = illu.image
                flag = 2
        else:
            try:
                download_url = detail.illust.meta_single_page.original_image_url
            except Exception:
                try:
                    # 获取原图失败 获取大图
                    download_url = detail.illust.image_urls.large
                    flag = 1
                except Exception:
                    # 获取大图失败，直接使用展示图
                    download_url = illu.image
                    flag = 2
        print("Download " + show_msg[flag])
        return download_url


class IlluDownloadThread(threading.Thread):
    def __init__(self, url, path=IMAGE_SAVE_BASEPATH, create_path=False, downloader=None):
        threading.Thread.__init__(self, name="Download-" + url)
        self.url = url
        self.path = path
        self.create_path = create_path
        self.downloader = downloader
        self.success = None
        self.fail = None
        self.callback_params = None

    def run(self):
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except Exception as e:
                error_log("make dir Fail:" + self.path)
                error_log(e)
                return
        try:
            path = ImageDownload.download_topics(self.url, self.path,
                                                 create_path=self.create_path, downloader=self.downloader)
            if self.success:
                self.success(CommonUtils.build_callback_msg(path, url=self.url))
                if self.callback_params and self.callback_params.has_key(
                        'current_count') and self.callback_params.has_key('all_count'):
                    current_count = self.callback_params['current_count'].getAndInc()
                    if self.callback_params['all_count'] == (current_count + 1):
                        self.success("Download from Pixivision:\n" +
                                     self.callback_params['url'] +
                                     "\nAll tasks are complete!\n\n")
        except Exception as e:
            print ("Download topics fail")
            print (e)
            if self.fail:
                self.fail()

    def register_hook(self, success_callback=None, fail_callback=None, params=None):
        if success_callback:
            self.success = success_callback
        if fail_callback:
            self.fail = fail_callback
        if params:
            self.callback_params = params
        return self
