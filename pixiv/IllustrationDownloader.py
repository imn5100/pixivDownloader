# -*- coding: utf-8 -*-
import os

from utils import CommonUtils
from utils.LoggerUtil import error_log

PAGE_LIMIT_CONTINUE = "P>limit"


class IllustrationDownloader(object):
    def __init__(self, api):
        self.api = api

    def download(self, illust_id, path, url):
        extension = os.path.splitext(url)[1]
        save_path = path + "/p_%s%s" % (illust_id, extension)
        print(save_path)
        return self.api.download(url, path=save_path)

    def download_by_detail(self, detail, path, p_limit=0):
        """
        通过api获取的插画详情 下载
        :param detail: 插画详情
        :param path:   下载路径
        :param p_limit: 插画p数(页数)限制 0代表不限制
        :return:
        """
        if detail:
            try:
                illust_id = detail.id
                # 普通插画
                if detail.page_count == 1:
                    try:
                        url = detail.meta_single_page.original_image_url
                    except Exception:
                        url = detail.image_urls.large
                    path = self.download(illust_id, path, url)
                # 多图插画
                else:
                    if 0 < p_limit < detail.page_count:
                        # 该插画P数大于最大限制，放弃下载
                        print("Pixiv id:%s P>limit,Skip download" % (illust_id,))
                        return PAGE_LIMIT_CONTINUE
                    urls = detail.meta_pages
                    # 获取多图
                    if len(urls) > 1:
                        # 多图放入一个文件夹中
                        path += "/p_%s" % illust_id
                        if not os.path.exists(path):
                            os.mkdir(path)
                        for index in range(len(urls)):
                            try:
                                url = urls[index].image_urls.original if \
                                    urls[index].image_urls.has_key("original") else urls[index].image_urls.large
                                extension = os.path.splitext(url)[1]
                                save_path = path + "/p_%s_%d%s" % (illust_id, index, extension)
                                print(save_path)
                                self.api.download(url, path=save_path)
                            except Exception:
                                continue
                        path = path + "/"
                    else:
                        # 获取多图失败,下载大图
                        url = detail.image_urls.large
                        path = self.download(illust_id, path, url)
                return path
            except Exception as e:
                error_log("Download fail:")
                error_log(e)

    def download_illustration(self, illu, path, p_limit=0):
        """
        通过程序构造的插画详情下载
        :param illu:  插画详情
        :param path:  下载路径
        :param p_limit: 插画p数(页数)限制 0代表不限制
        :return:
        """
        if illu.has_key("url") and illu.has_key("title"):
            illust_id = CommonUtils.get_url_param(illu.url, "illust_id")
            detail = self.api.illust_detail(illust_id)
            if detail:
                try:
                    detail = detail.illust
                    # 普通插画
                    if detail.page_count == 1:
                        try:
                            url = detail.meta_single_page.original_image_url
                        except Exception:
                            url = detail.image_urls.large
                        path = self.download(illust_id, path, url)
                    # 多图插画
                    else:
                        if 0 < p_limit < detail.page_count:
                            # 该插画P数大于最大限制，放弃下载
                            print("Pixiv id:%s, P>limit,Skip download" % (illust_id,))
                            return PAGE_LIMIT_CONTINUE
                        urls = detail.meta_pages
                        # 获取多图
                        if len(urls) > 1:
                            # 多图放入一个文件夹中
                            path += "/p_%s" % illust_id
                            if not os.path.exists(path):
                                os.mkdir(path)
                            for index in range(len(urls)):
                                try:
                                    url = urls[index].image_urls.original if \
                                        urls[index].image_urls.has_key("original") else urls[index].image_urls.large
                                    extension = os.path.splitext(url)[1]
                                    save_path = path + "/p_%s_%d%s" % (illust_id, index, extension)
                                    print(save_path)
                                    self.api.download(url, path=save_path)
                                except Exception:
                                    continue
                            path = path + "/"
                        else:
                            # 获取多图失败,下载大图
                            url = detail.image_urls.large
                            path = self.download(illust_id, path, url)
                    return path
                except Exception as e:
                    error_log("Download fail:")
                    error_log(e)
            else:
                print(illu.title + " can't get detail id :" + illust_id)
        else:
            return

    def download_all_by_id(self, illust_id, path, p_limit=0):
        """
        通过pixiv id下载插画
        :param illust_id: id
        :param path:  下载路径
        :param p_limit: 是否限制插画p数(页数)
        :return:
        """
        detail = self.api.illust_detail(illust_id)
        if detail:
            try:
                detail = detail.illust
                # 普通插画
                if detail.page_count == 1:
                    try:
                        url = detail.meta_single_page.original_image_url
                    except Exception:
                        url = detail.image_urls.large
                    extension = os.path.splitext(url)[1]
                    save_path = path + "/p_%s%s" % (illust_id, extension)
                    print("Downloading:" + save_path)
                    path = self.api.download(url, path=save_path)
                # 多图插画
                else:
                    if 0 < p_limit < detail.page_count:
                        # 该插画P数大于最大限制，放弃下载
                        print("Pixiv id:%s P>limit,Skip download" % (illust_id,))
                        return PAGE_LIMIT_CONTINUE
                    urls = detail.meta_pages
                    # 获取多图
                    if len(urls) > 1:
                        # 多图放入一个文件夹中
                        path += "/p_%s" % illust_id
                        if not os.path.exists(path):
                            os.mkdir(path)
                        for index in range(len(urls)):
                            try:
                                url = urls[index].image_urls.original if \
                                    urls[index].image_urls.has_key("original") else urls[index].image_urls.large
                                extension = os.path.splitext(url)[1]
                                save_path = path + "/p_%s_%d%s" % (illust_id, index, extension)
                                print("Downloading:" + save_path)
                                self.api.download(url, path=save_path)
                            except Exception:
                                continue
                        path = path + "/"
                    else:
                        # 获取多图失败,下载大图
                        url = detail.image_urls.large
                        path = self.api.download(url, prefix=path)
                return path
            except Exception as e:
                error_log("Download fail:" + detail)
                error_log(e)
        else:
            print(" can't get detail id :" + str(illust_id))

    def download_all_by_url(self, url, prefix):
        illust_id = CommonUtils.get_url_param(url, "illust_id")
        if illust_id:
            return self.download_all_by_id(illust_id, prefix)
        else:
            return self.api.download(url.strip(), prefix=prefix)
