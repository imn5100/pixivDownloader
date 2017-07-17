# -*- coding: utf-8 -*-
import re

import requests

from pixiv.PixivHtmlParser import PixivHtmlParser
from pixiv_config import PIXIV_LOGIN_KEY, PIXIV_PAGE_HEADERS, PIXIV_LOGIN_URL, RETRY_TIME, TIMEOUT, PIXIV_SEARCH_URL, \
    DOWNLOAD_THRESHOLD
from pixivapi.PixivUtils import parse_resp, PixivError


def get_post_key(content):
    if content:
        postkey_str = re.search('name="post_key" value="\w*"', content)
        if postkey_str:
            return postkey_str.group().split('"')[-2]
    else:
        return None


class PixivDataHandler(object):
    def __init__(self, username=None, password=None, cookies=None):
        self.session = requests.session()
        if username and password:
            self.username = username
            self.password = password
            self.login()
        elif cookies:
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        else:
            raise PixivError('Please input username and password  or  input cookies!')

    # 模拟页面登录pixiv
    def login(self):
        r = self.session.get(PIXIV_LOGIN_KEY, headers=PIXIV_PAGE_HEADERS)
        if r.ok:
            post_key = get_post_key(r.content)
            if post_key:
                post_data = {
                    'pixiv_id': self.username,
                    'password': self.password,
                    'post_key': post_key,
                    'source': 'accounts'
                }
            response = self.session.post(PIXIV_LOGIN_URL, data=post_data, headers=PIXIV_PAGE_HEADERS)
            res_obj = parse_resp(response)
            # 返回json 抽风了，一下successed,一下success 这里都验证一下
            if res_obj.body.has_key("successed") or res_obj.body.has_key("success"):
                print("Login Success getCookies:" + str(requests.utils.dict_from_cookiejar(self.session.cookies)))
                return self.session
            else:
                raise PixivError('username or password wrong!.')
        else:
            print('get post_key error')

    # 获取pixiv页面
    def request_page(self, url, encoding='utf-8'):
        count = 0  # 失败重试次数
        while count <= RETRY_TIME:
            try:
                r = self.session.get(url=url, timeout=TIMEOUT)
                r.encoding = encoding
                if (not r.ok) or len(r.content) < 300:
                    count += 1
                    continue
                else:
                    return r.text
            except Exception:
                count += 1
                continue
        return None

    def search(self, word, page=1, search_type='illust', download_threshold=DOWNLOAD_THRESHOLD):
        if word:
            url = (PIXIV_SEARCH_URL % (word, search_type, int(page)))
        else:
            raise PixivError('search word can not be null')
        print(url)
        html = self.request_page(url)
        if not html:
            print("Get Page is None!URL:" + url)
            return []
        search_result = PixivHtmlParser.parse_search_result(html)
        pop_result = PixivHtmlParser.parse_popular_introduction(html)
        if not pop_result:
            pop_result = []
        if search_result:
            # 过滤数据不完整和收藏数不超过阈值的插画信息
            search_result = filter(
                lambda data: (data.has_key("url") and data.has_key("title") and data.has_key("mark_count") and int(
                    data.mark_count) >= download_threshold),
                search_result)
            pop_result.extend(search_result)
        return pop_result
