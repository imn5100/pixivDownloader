# -*- coding: utf-8 -*-
import os
from Queue import Queue
from threading import Thread

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


def download_queue(queue, path, auth_api):
    while True:
        try:
            illust_list = queue.get()
            download_topics(illust_list, path, auth_api)
        except Exception, e:
            print(e)
            continue
        finally:
            queue.task_done()


if __name__ == '__main__':
    username = "*"
    password = "*"
    data_handler = PixivDataDownloader.PixivDataHandler(username, password)
    auth_api = AuthPixivApi(username, password)
    page = 5
    queue = Queue()
    for i in range(page):
        t = Thread(target=download_queue, args=(queue, "E://download", auth_api))
        t.daemon = True
        t.start()
    for p in range(1, page):
        result = data_handler.search("みぅな", page=p)
        print(result)
        queue.put(result)
    queue.join()
