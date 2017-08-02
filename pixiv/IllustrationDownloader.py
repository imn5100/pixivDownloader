# -*- coding: utf-8 -*-
import os

from pixiv_config import IMAGE_USE_ORG_NAME, P_LIMIT
from utils import CommonUtils
from utils.LoggerUtil import error_log


class IllustrationDownloader(object):
    def __init__(self, api):
        self.api = api

    def download(self, illust_id, title, path, url):
        extension = os.path.splitext(url)[1]
        if IMAGE_USE_ORG_NAME:
            save_path = path + "/p_%s_%s%s" % (
                illust_id, CommonUtils.filter_dir_name(title), extension)
        else:
            save_path = path + "/p_%s%s" % (illust_id, extension)
        print(save_path)
        return self.api.download(url, path=save_path)

    def download_illustration(self, illu, path, p_limit=P_LIMIT):
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
                        except:
                            url = detail.image_urls.large
                        path = self.download(illust_id, illu.title, path, url)
                    # 多图插画
                    else:
                        if 0 < p_limit < detail.page_count:
                            # 该插画P数大于最大限制，放弃下载
                            print("Pixiv id:%s,name:%s P>limit,Skip download" % (illust_id, illu.title))
                            return
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
                                    if IMAGE_USE_ORG_NAME:
                                        save_path = path + "/p_%s_%s_%d%s" % (
                                            illust_id,
                                            CommonUtils.filter_dir_name(illu.title),
                                            index, extension)
                                    else:
                                        save_path = path + "/p_%s_%d%s" % (illust_id, index, extension)
                                    print(save_path)
                                    self.api.download(url, path=save_path)
                                except:
                                    continue
                            path = path + "/"
                        else:
                            # 获取多图失败,下载大图
                            url = detail.image_urls.large
                            path = self.download(illust_id, illu.title, path, url)
                    return path
                except Exception as e:
                    error_log("Download fail:")
                    error_log(e)
            else:
                print(illu.title + " can't get detail id :" + illust_id)
        else:
            return

    def download_all_by_id(self, illust_id, path, limit_p=True):
        detail = self.api.illust_detail(illust_id)
        if detail:
            try:
                detail = detail.illust
                # 普通插画
                if detail.page_count == 1:
                    try:
                        url = detail.meta_single_page.original_image_url
                    except:
                        url = detail.image_urls.large
                    extension = os.path.splitext(url)[1]
                    save_path = path + "/p_%s%s" % (illust_id, extension)
                    print("Downloading:" + save_path)
                    path = self.api.download(url, path=save_path)
                # 多图插画
                else:
                    if detail.page_count > P_LIMIT and limit_p:
                        # 该插画P数大于最大限制，放弃下载
                        print("Pixiv id:%s P>limit,Skip download" % (illust_id,))
                        return
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
                            except:
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
