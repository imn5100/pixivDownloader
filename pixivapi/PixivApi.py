# -*- coding:utf-8 -*-
import threading

from pixiv_config import USERNAME, PASSWORD, ACCESS_TOKEN, REFRESH_TOKEN
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
            success = False
            if not cls.__apiClient:
                if ACCESS_TOKEN:
                    try:
                        cls.__apiClient = AuthPixivApi(None, None, access_token=ACCESS_TOKEN)
                    except Exception as e:
                        print (e)
                    else:
                        if cls.__apiClient and cls.__apiClient.check_login_success():
                            success = True

                if not success:
                    try:
                        cls.__apiClient = AuthPixivApi(USERNAME, PASSWORD, refresh_token=REFRESH_TOKEN)
                    except Exception as e:
                        print (e)
                    else:
                        if cls.__apiClient and cls.__apiClient.check_login_success():
                            success = True

                if not success:
                    raise PixivError("[ERROR] auth() failed! Please check username and password or token")
        except Exception as e:
            raise e
        finally:
            cls.__lock.release()
