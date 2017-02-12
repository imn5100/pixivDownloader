# -*- coding: utf-8 -*-
import os

from pixiv_config import IMAGE_USE_ORG_NAME, P_LIMIT
from pixivapi.PixivApi import PixivApi
from utils import CommonUtils
from utils.LoggerUtil import error_log


def download(illust_id, title, path, url, auth_api):
    extension = os.path.splitext(url)[1]
    if IMAGE_USE_ORG_NAME:
        save_path = path + "/p_%s_%s%s" % (
            illust_id, CommonUtils.filter_dir_name(title), extension)
    else:
        save_path = path + "/p_%s%s" % (illust_id, extension)
    print(save_path)
    auth_api.download(url, path=save_path)


def download_illustration(illu, path, auth_api):
    """
    #illu 包含插画详细
    path 存储路径
    auth_api 具有身份验证的下载工具
    """
    if illu.has_key("url") and illu.has_key("title"):
        illust_id = CommonUtils.get_url_param(illu.url, "illust_id")
        detail = PixivApi.illust_detail(illust_id)
        if detail:
            try:
                detail = detail.illust
                # 普通插画
                if detail.page_count == 1:
                    try:
                        url = detail.meta_single_page.original_image_url
                    except:
                        url = detail.image_urls.large
                    download(illust_id, illu.title, path, url, auth_api)
                # 多图插画
                else:
                    if detail.page_count > P_LIMIT:
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
                                auth_api.download(url, path=save_path)
                            except:
                                continue
                    else:
                        # 获取多图失败,下载大图
                        url = detail.image_urls.large
                        download(illust_id, illu.title, path, url, auth_api)
            except Exception, e:
                error_log("Download fail:")
                error_log(e)
        else:
            print(illu.title + " can't get detail id :" + illust_id)
    else:
        return


def download_queue(queue, path, auth_api):
    while True:
        try:
            illustration = queue.get()
            download_illustration(illustration, path, auth_api)
        except Exception, e:
            print(e)
            continue
        finally:
            queue.task_done()
