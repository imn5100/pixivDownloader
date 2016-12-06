# -*- coding: utf-8 -*-
import re
import requests
from pixiv_config import *
from BeautifulSoup import BeautifulSoup

from pixivapi.PixivUtils import parse_obj


class HtmlDownloader(object):
    @classmethod
    def download(cls, url, encoding='utf-8'):
        count = 0  # 失败重试次数
        while count <= RETRY_TIME:
            try:
                r = requests.get(url=url, headers=HEADER, timeout=TIMEOUT)
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

    @classmethod
    def parse_illustration_list(cls, html):
        if not html:
            return None
        main = BeautifulSoup(html)
        lis = main.findAll("li", attrs={"class": "article-card-container"})
        datas = []
        for li in lis:
            try:
                data = {"label": li.find("span",
                                         attrs={"class": "arc__thumbnail-label _category-label large spotlight"}).text}
                a = li.find("h2", attrs={"class": "arc__title "}).find("a")
                data["href"] = BASE_URL + a["href"]
                data["title"] = a.text
                data["pub_time"] = li.find("time").text
                data["tags"] = []
                tags = li.findAll("div", attrs={"class": "tls__list-item small"})
                for tag in tags:
                    data["tags"].append(tag.text)
                data = parse_obj(data)
                datas.append(data)
            except Exception, e:
                print(e.message)
                continue
        return datas

    @classmethod
    def parse_illustration(cls, html):
        if not html:
            return None
        main = BeautifulSoup(html)
        divs = main.findAll("div", attrs={"class": re.compile('am__work gtm__illust-collection-illusts-\d*')})
        datas = []
        for div in divs:
            try:
                data = {}
                author_a = div.find("a", attrs={"class": "author-img-container inner-link"})
                title_a = div.find("h3", attrs={"class": "am__work__title"}).find("a")
                data["author"] = author_a.text
                data["author_page"] = author_a['href']
                data["title"] = title_a.text
                data["image_page"] = title_a["href"]
                data["image"] = div.find("img", attrs={"class": "am__work__illust "})["src"]
                data = parse_obj(data)
                datas.append(data)
            except Exception, e:
                print(e.message)
                continue
        return datas
