# -*- coding:utf-8 -*-
import os
import shutil

import requests

import pixiv_config
from PixivUtils import *


class PixivApi(object):
    @classmethod
    def download(cls, url, prefix='', path=None, referer='https://app-api.pixiv.net/'):
        if not path:
            path = prefix + os.path.basename(url)
        response = requests.get(url, headers={'Referer': referer}, stream=True)
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    # 获取作品详情
    @classmethod
    def illust_detail(cls, illust_id):
        url = pixiv_config.ILLUST_DETAIL
        params = {
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 'true',
            'illust_id': illust_id
        }
        response = requests.get(url, params, headers=pixiv_config.HEADER, timeout=5)
        if response.ok and len(response.content) > 10:
            return parse_resp(response)
        else:
            return None

    # 获取关联作品
    @classmethod
    def illust_related(cls, illust_id, seed_illust_ids=None):
        url = pixiv_config.ILLUST_RELATED
        params = {
            'illust_id': illust_id,
        }
        if type(seed_illust_ids) == str:
            params['seed_illust_ids'] = seed_illust_ids
        if type(seed_illust_ids) == list:
            params['seed_illust_ids'] = ",".join([str(iid) for iid in seed_illust_ids])
        r = requests.get(url, params, headers=pixiv_config.HEADER)
        return parse_resp(r)
