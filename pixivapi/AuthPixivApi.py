# -*- coding:utf-8 -*-
import os

import requests
import shutil

import time

import pixiv_config
from pixivapi.PixivUtils import PixivError, parse_json, parse_resp


def requests_call(method, url, **kwargs):
    try:
        if method.upper() == 'GET':
            return requests.get(url, **kwargs)
        elif method.upper() == 'POST':
            return requests.post(url, **kwargs)
        elif method.upper() == 'DELETE':
            return requests.delete(url, **kwargs)
    except Exception as e:
        raise PixivError('requests %s %s error: %s' % (method, url, e))
    raise PixivError('Unknow method: %s' % method)


# 需要经过登录后才能使用的api端
class AuthPixivApi(object):
    def __init__(self, username, password, access_token=None):
        self.username = username
        self.password = password
        self.access_token = access_token
        self.user_id = None
        self.refresh_token = None
        if not access_token:
            self.login(username, password)

    def require_auth(self):
        if self.access_token is None:
            raise PixivError('Authentication required! Call login() first!')

    def auth_requests_call(self, method, url, headers={}, **kwargs):
        self.require_auth()
        headers['Referer'] = 'http://spapi.pixiv.net/'
        headers['User-Agent'] = 'PixivIOSApp/6.0.9'
        # 指定语言
        # ja  日文
        # zh 中文简体
        # zh-tw 中文繁体
        # en 或空或其他无法解析语言 英文
        headers['Accept-Language'] = 'en'
        headers['Authorization'] = 'Bearer %s' % self.access_token
        response = requests_call(method, url, headers=headers, **kwargs)
        if response.status_code != 200:
            print response.content
            raise PixivError(response.content)
        return response

    def login(self, username, password):
        return self.auth(username=username, password=password)

    def auth(self, username=None, password=None, refresh_token=None):
        url = 'https://oauth.secure.pixiv.net/auth/token'
        headers = {
            'App-OS': 'ios',
            'App-OS-Version': '9.3.3',
            'App-Version': '6.0.9',
            'User-Agent': 'PixivIOSApp/6.0.9 (iOS 9.3.3; iPhone8,1)',
        }
        data = {
            'get_secure_url': 1,
            'client_id': 'bYGKuGVw91e0NMfPGp44euvGt59s',
            'client_secret': 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK',
        }
        if (username is not None) and (password is not None):
            data['grant_type'] = 'password'
            data['username'] = username
            data['password'] = password
        elif (refresh_token is not None) or (self.refresh_token is not None):
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = refresh_token or self.refresh_token
        else:
            raise PixivError('[ERROR] auth() but no password or refresh_token is set.')
        r = requests.post(url, headers=headers, data=data)
        if r.status_code not in [200, 301, 302]:
            if data['grant_type'] == 'password':
                raise PixivError(
                    '[ERROR] auth() failed! check username and password.\nHTTP %s: %s' % (r.status_code, r.text),
                    header=r.headers, body=r.text)
            else:
                raise PixivError('[ERROR] auth() failed! check refresh_token.\nHTTP %s: %s' % (r.status_code, r.text),
                                 header=r.headers, body=r.text)
        token = None
        try:
            token = parse_json(r.text)
            self.access_token = token.response.access_token
            self.user_id = token.response.user.id
            self.refresh_token = token.response.refresh_token
        except:
            raise PixivError('Get access_token error! Response: %s' % (token), header=r.headers, body=r.text)
        print token.response.access_token
        return token

    def download(self, url, prefix='', path=None):
        if not path:
            path = prefix + os.path.basename(url)
        if os.path.exists(path) and (not pixiv_config.OVERRIDE_IMAGE):
            print("continue!")
            return path
        response = self.auth_requests_call("get", url, timeout=60, stream=True)
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        return path

    def search_works(self, query, page=1, per_page=10, mode='text',
                     period='all', order='desc', sort='date',
                     types=['illustration', 'manga', 'ugoira'],
                     image_sizes=['large'],  # 'px_128x128', 'px_480mw',
                     include_stats=True, include_sanity_level=True):
        url = 'https://public-api.secure.pixiv.net/v1/search/works.json'
        params = {
            'q': query,
            'page': page,
            'per_page': per_page,
            'period': period,
            'order': order,
            'sort': sort,
            'mode': mode,
            'types': ','.join(types),
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
        }
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    def illust_detail(self, illust_id):
        url = pixiv_config.ILLUST_DETAIL
        params = {
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 'true',
            'illust_id': illust_id
        }
        count = 0  # 失败重试次数
        while count <= pixiv_config.RETRY_TIME:
            try:
                response = self.auth_requests_call('GET', url, params=params, timeout=8)
                if response.ok and len(response.content) > 10:
                    return parse_resp(response)
                else:
                    return None
            # 多线程请求，容易被拒绝设置重试三次，每次重试间隔2s
            except Exception:
                time.sleep(2)
                count += 1
                continue
            except PixivError, e:
                raise e
                break
