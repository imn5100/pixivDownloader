# -*- coding: utf-8 -*-
import re
import json

from BeautifulSoup import BeautifulSoup

from pixiv_config import PIXIV_URL
from pixivapi.PixivUtils import parse_dict


class PixivHtmlParser(object):
    @classmethod
    def parse_search_result(cls, html):
        if not html:
            return None
        main = BeautifulSoup(html)
        result_list = main.find("input", attrs={"id": "js-mount-point-search-result-list"})
        datas = []
        if input:
            try:
                json_str = str(result_list['data-items']).replace('&quot;', '"').replace("&quotquot;", '"')
                if not json_str or len(json_str) <= 0:
                    print("search normal result is empty")
                    return datas
                items = json.loads(json_str)
                if items and len(items) > 0:
                    for item in items:
                        user = {
                            "name": item['userName'],
                            "id": item['userId'],
                        }
                        data = {
                            "url": item['url'],
                            "title": item['illustTitle'],
                            "id": item['illustId'],
                            "mark_count": item['bookmarkCount'],
                            'user': user
                        }
                        datas.append(parse_dict(data))
            except Exception:
                print("search normal result is empty")
        return datas

    @classmethod
    def parse_popular_introduction(cls, html):
        if not html:
            return None
        main = BeautifulSoup(html)
        section = main.find("div", attrs={"class": "_premium-lead-popular-d-body"})
        datas = []
        if not section:
            print("search popular result is empty")
            return datas
        lis = section.findAll("li", attrs={"class": re.compile("image-item\s*")})
        if not lis:
            print("search popular result is empty")
            return datas
        for li in lis:
            try:
                data = {"url": PIXIV_URL + li.find("a", attrs={"class": re.compile("work  _work\w*")})["href"],
                        "title": li.find("h1", attrs={"class": "title"}).text}
                data = parse_dict(data)
                datas.append(data)
            except Exception as e:
                print("parse_popular_introduction Warning:")
                print(e.message)
                continue
        return datas
