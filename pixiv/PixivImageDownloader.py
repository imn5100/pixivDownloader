# -*- coding: utf-8 -*-
import os

from pixiv import PixivDataDownloader
from pixiv_config import IMAGE_USE_ORG_NAME
from pixivapi.AuthPixivApi import AuthPixivApi
from pixivapi.PixivApi import PixivApi
from utils import CommonUtils
from utils.LoggerUtil import error_log


def download_topics(illu_list, path, auth_api):
    if not illu_list:
        return
    for illu in illu_list:
        if illu.has_key("url") and illu.has_key("title"):
            id = CommonUtils.get_url_param(illu.url, "illust_id")
            detail = PixivApi.illust_detail(id)
            if detail:
                try:
                    detail = detail.illust
                    if detail.page_count == 1:
                        try:
                            url = detail.meta_single_page.original_image_url
                        except:
                            url = detail.image_urls.large
                    else:
                        url = detail.image_urls.large
                    extension = os.path.splitext(url)[1]
                    if IMAGE_USE_ORG_NAME:
                        save_path = path + "/p_%s_%s%s" % (id, CommonUtils.filter_dir_name(illu.title), extension)
                    else:
                        save_path = path + "/p_%s%s" % (id, extension)
                    print(save_path)
                    auth_api.download(url, path=save_path)
                except Exception, e:
                    error_log("Download fail:")
                    error_log(e)
            else:
                print(illu.title + " can't get detail id :" + id)
        else:
            continue


if __name__ == '__main__':
    username = "*@QQ.COM"
    password = "*"
    data_handler = PixivDataDownloader.PixivDataHandler(username, password)
    auth_api = AuthPixivApi(username, password)
    for p in range(1, 3):
        result = data_handler.search("miku", page=p)
        print(result)
        download_topics(result, "E://download/", auth_api)
