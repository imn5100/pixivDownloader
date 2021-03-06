# -*- coding:utf-8 -*-
import os

import requests
import shutil

import time

import pixiv_config
from pixivapi.PixivUtils import PixivError, parse_json, parse_resp
from utils import CommonUtils
from utils.CommonUtils import format_bool


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
    def __init__(self, username, password, access_token=None, refresh_token=None, use_proxy=pixiv_config.USE_PROXY):
        self.username = username
        self.password = password
        self.user_id = None
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.use_proxy = use_proxy
        if use_proxy and len(pixiv_config.PROXIES) == 0:
            raise PixivError('Proxy config Error')
        if CommonUtils.is_empty(access_token):
            self.login(username, password, refresh_token)

    def require_auth(self):
        if self.access_token is None:
            raise PixivError('Authentication required! Call login() first!')

    def auth_requests_call(self, method, url, headers=None, use_proxy_method=True, **kwargs):
        if headers is None:
            headers = {}
        self.require_auth()
        headers['Referer'] = 'http://spapi.pixiv.net/'
        headers['User-Agent'] = 'PixivIOSApp/6.0.9'
        # 指定语言
        # ja  日文
        # zh 中文简体
        # zh-tw 中文繁体
        # en 或空或其他无法解析语言 英文
        headers['Accept-Language'] = 'zh'
        headers['Authorization'] = 'Bearer %s' % self.access_token
        # 先判断全局是否使用代理，再判断方法是否使用代理
        if self.use_proxy:
            if use_proxy_method:
                response = requests_call(method, url, proxies=pixiv_config.PROXIES, headers=headers, **kwargs)
            else:
                response = requests_call(method, url, headers=headers, **kwargs)
        else:
            response = requests_call(method, url, headers=headers, **kwargs)
        if response.status_code != 200:
            raise PixivError(response.content)
        response.encoding = 'utf-8'
        return response

    def login(self, username=None, password=None, refresh_token=None):
        return self.auth(username=username, password=password, refresh_token=refresh_token)

    def auth(self, username=None, password=None, refresh_token=None):
        url = 'https://oauth.secure.pixiv.net/auth/token'
        headers = {
            'App-OS': 'ios',
            'App-OS-Version': '10.3.1',
            'App-Version': '6.8.3',
            'User-Agent': 'PixivIOSApp/6.8.3 (iOS 10.3.1; iPhone8,1)',
        }
        data = {
            'get_secure_url': 1,
            'client_id': 'MOBrBDS8blbauoSck0ZfDbtuzpyT',
            'client_secret': 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj',
        }
        if CommonUtils.is_not_empty(username) and CommonUtils.is_not_empty(password):
            data['grant_type'] = 'password'
            data['username'] = username
            data['password'] = password
        elif (refresh_token is not None) or (self.refresh_token is not None):
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = refresh_token or self.refresh_token
        else:
            raise PixivError('[ERROR] auth() but no password or refresh_token is set.')
        r = requests.post(url, headers=headers, data=data, proxies=pixiv_config.PROXIES)
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
        except Exception as e:
            print (e)
            raise PixivError('Get access_token error! Response: %s' % token, header=r.headers, body=r.text)
        print ("ACCESS TOKEN " + self.access_token)
        print ("ACCESS Refresh Token " + self.refresh_token)
        return token

    def download(self, url, prefix='', path=None):
        if not path:
            path = prefix + os.path.basename(url)
        if os.path.exists(path) and (not pixiv_config.OVERRIDE_IMAGE):
            print("continue!")
            return path
        response = self.auth_requests_call("get", url, use_proxy_method=pixiv_config.DOWNLOAD_USE_PROXY, timeout=60,
                                           stream=True)
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        return path

    # 作品详细1
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
                response = self.auth_requests_call('GET', url, params=params, timeout=60)
                if response.ok and len(response.content) > 10:
                    return parse_resp(response)
                else:
                    return None
            # 多线程请求，容易被拒绝设置重试三次，每次重试间隔2s
            except PixivError as e:
                print (e)
                break
            except Exception:
                time.sleep(2)
                count += 1
                continue

    def check_login_success(self):
        url = pixiv_config.ILLUST_DETAIL
        params = {
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 'true',
            'illust_id': 55418
        }
        try:
            response = self.auth_requests_call('GET', url, params=params, timeout=60)
            if response.ok and len(response.content) > 10:
                return True
            else:
                return False
        except Exception:
            return False

    # search_target - 搜索类型
    #   partial_match_for_tags  - 标签部分一致
    #   exact_match_for_tags    - 标签完全一致
    #   title_and_caption       - 标题说明文
    # sort: [date_desc, date_asc]
    # duration: [within_last_day, within_last_week, within_last_mont
    def search_illust(self, word, search_target='partial_match_for_tags', sort='date_desc', duration=None,
                      illust_filter='for_ios', offset=None):
        url = 'https://app-api.pixiv.net/v1/search/illust'
        params = {
            'word': word,
            'search_target': search_target,
            'sort': sort,
            'filter': illust_filter,
        }
        if duration:
            params['duration'] = duration
        if offset:
            params['offset'] = offset
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    def search_popular_illust(self, word, search_target='partial_match_for_tags', sort='date_desc', duration=None,
                              illust_filter='for_ios', offset=None):
        url = 'https://app-api.pixiv.net/v1/search/popular-preview/illust'
        params = {
            'word': word,
            'search_target': search_target,
            'sort': sort,
            'filter': illust_filter,
        }
        if duration:
            params['duration'] = duration
        if offset:
            params['offset'] = offset
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    # spotlight rename  to  pixivision  category = illust
    def spotlight(self, category='all', illust_filter='for_ios', offset=None):
        url = 'https://app-api.pixiv.net/v1/spotlight/articles'
        params = {
            'filter': illust_filter,
        }
        if category:
            params['category'] = category
        if offset:
            params['offset'] = offset
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    # 相关作品列表 filter : for_ios or for_android   not login
    def illust_related(self, illust_id, illust_filter=None, seed_illust_ids=None):
        url = 'https://app-api.pixiv.net/v2/illust/related'
        params = {
            'illust_id': illust_id,
        }
        if illust_filter:
            params['filter'] = illust_filter
        if type(seed_illust_ids) == str:
            params['seed_illust_ids[]'] = [seed_illust_ids]
        if type(seed_illust_ids) == list:
            params['seed_illust_ids[]'] = seed_illust_ids
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    # 推荐作品
    def illust_recommended(self, content_type='illust', include_ranking_label=True, illust_filter='for_ios',
                           max_bookmark_id_for_recommend=None, min_bookmark_id_for_recent_illust=None,
                           offset=None, include_ranking_illusts=None):
        url = 'https://app-api.pixiv.net/v1/illust/recommended'
        params = {
            'content_type': content_type,
            'include_ranking_label': format_bool(include_ranking_label),
            'filter': illust_filter,
        }
        if max_bookmark_id_for_recommend:
            params['max_bookmark_id_for_recommend'] = max_bookmark_id_for_recommend
        if min_bookmark_id_for_recent_illust:
            params['min_bookmark_id_for_recent_illust'] = min_bookmark_id_for_recent_illust
        if offset:
            params['offset'] = offset
        if include_ranking_illusts:
            params['include_ranking_illusts'] = CommonUtils.format_bool(include_ranking_illusts)

        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    #  not login
    def app_ranking(self, mode='day', date=None,
                    include_stats=True, include_sanity_level=True, offset=None):
        """
        排行榜/过去排行榜
        :param mode:
        day(每日）day_male(每日男性) day_female(每日女性) week_original(原创) week_rookie(新人) week(每周)  month(每月) day_r18  week_r18
        :param date:
        '2015-04-01' (过去排行榜)
        :param include_stats:
        :param include_sanity_level:
        :param offset:
        :return:
        """
        url = 'https://app-api.pixiv.net/v1/illust/ranking'
        params = {
            'mode': mode,
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
        }
        if offset:
            params['offset'] = offset
        if date:
            params['date'] = date
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    # pixiv public api

    # 排行榜/过去排行榜
    # ranking_type: [all, illust, manga, ugoira]
    # mode: [daily, weekly, monthly, rookie, original, male, female, daily_r18, weekly_r18, male_r18, female_r18, r18g]
    #       for 'illust' & 'manga': [daily, weekly, monthly, rookie, daily_r18, weekly_r18, r18g]
    #       for 'ugoira': [daily, weekly, daily_r18, weekly_r18],
    # page: [1-n]
    # date: '2015-04-01' (仅过去排行榜)
    def ranking(self, ranking_type='all', mode='daily', page=1, per_page=10, date=None,
                image_sizes=None,
                include_stats=True, include_sanity_level=True):
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        url = 'https://public-api.secure.pixiv.net/v1/ranking/%s.json' % ranking_type
        params = {
            'mode': mode,
            'page': page,
            'per_page': per_page,
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
            'profile_image_sizes': ','.join(['px_170x170', 'px_50x50']),
        }
        if date:
            params['date'] = date
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    # search
    def search_works(self, query, page=1, per_page=10, mode='text',
                     period='all', order='desc', sort='date',
                     types=None,
                     image_sizes=None,
                     include_stats=True, include_sanity_level=True):
        if image_sizes is None:
            image_sizes = ['large']
        if types is None:
            types = ['illustration', 'manga', 'ugoira']
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

    # 作品详细2
    def works(self, illust_id):
        url = 'https://public-api.secure.pixiv.net/v1/works/%d.json' % illust_id
        params = {
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 'true',
        }
        r = self.auth_requests_call('GET', url, params=params)
        return parse_resp(r)

    @staticmethod
    def get_authApi_by_token():
        api = None
        success = False
        if pixiv_config.ACCESS_TOKEN:
            try:
                api = AuthPixivApi(None, None, pixiv_config.ACCESS_TOKEN)
            except Exception as e:
                print (e)
            if api and api.check_login_success():
                success = True
                print ("Access Token is correct!")
            else:
                api = None
                print ("Access Token error or expired!")

        if pixiv_config.REFRESH_TOKEN and not success:
            try:
                api = AuthPixivApi(None, None, refresh_token=pixiv_config.REFRESH_TOKEN)
            except Exception as e:
                print (e)
            if api and api.check_login_success():
                print ("Refresh Token is correct!")
            else:
                api = None
                print ("Access Token config error or expired!")
        return api

    def get(self, url):
        return parse_resp(self.auth_requests_call('GET', url))
