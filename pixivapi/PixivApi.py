# -*- coding:utf-8 -*-

import pixiv_config
from pixivapi.AuthPixivApi import AuthPixivApi


class PixivApi(object):
    __apiClient = None

    @classmethod
    def download(cls, url, prefix='', path=None, referer='https://app-api.pixiv.net/'):
        cls.check_api()
        return cls.__apiClient.download(url, prefix=prefix, path=path)

    # 获取作品详情
    @classmethod
    def illust_detail(cls, illust_id):
        cls.check_api()
        return cls.__apiClient.illust_detail(illust_id)

    @classmethod
    def check_api(cls):
        if not cls.__apiClient:
            cls.__apiClient = AuthPixivApi(pixiv_config.USERNAME, pixiv_config.PASSWORD,
                                           access_token=pixiv_config.ACCESS_TOKEN)
