# -*- coding:utf-8 -*-
import threading

from pixiv_config import USERNAME, PASSWORD
from pixivapi.AuthPixivApi import AuthPixivApi
from pixivapi.PixivUtils import PixivError


class PixivApi(object):
    __apiClient = None
    __lock = threading.Lock()

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
        if cls.__apiClient:
            return
        try:
            cls.__lock.acquire()
            if not cls.__apiClient:
                cls.__apiClient = AuthPixivApi.get_authApi_by_token()
                if cls.__apiClient is None:
                    cls.__apiClient = AuthPixivApi(USERNAME, PASSWORD)
                    if cls.__apiClient and not cls.__apiClient.check_login_success():
                        raise PixivError('[ERROR] auth() failed! Please check username and password')
        except Exception as e:
            raise e
        finally:
            cls.__lock.release()
