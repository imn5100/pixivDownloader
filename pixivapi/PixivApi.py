# -*- coding:utf-8 -*-

import pixiv_config
from pixivapi.AuthPixivApi import AuthPixivApi


# Deprecated pixiv api 需要登录才能请求到内容,暂时使用AuthPixivApi 替换方法实现，此类最终将弃用。
class PixivApi(object):
    apiClient = AuthPixivApi(pixiv_config.USERNAME, pixiv_config.PASSWORD, access_token=pixiv_config.ACCESS_TOKEN)

    @classmethod
    def download(cls, url, prefix='', path=None, referer='https://app-api.pixiv.net/'):
        return PixivApi.apiClient.download(url, prefix=prefix, path=path)

    # 获取作品详情
    @classmethod
    def illust_detail(cls, illust_id):
        return PixivApi.apiClient.illust_detail(illust_id)
