# -*- coding: utf-8 -*-
import re
import requests
from pixiv_config import *
from BeautifulSoup import BeautifulSoup

from pixivapi.PixivUtils import parse_dict


class HtmlDownloader(object):
    @classmethod
    def download(cls, url, encoding='utf-8'):
        count = 0  # 失败重试次数
        while count <= RETRY_TIME:
            try:
                r = requests.get(url=url, headers=CRAWLER_HEADER, timeout=TIMEOUT)
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

    # 获取pixivsion 插画专题列表
    @classmethod
    def parse_illustration_topic(cls, html):
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
                data = parse_dict(data)
                datas.append(data)
            except Exception, e:
                print("Get Topics Warning" + e.message)
                continue
        return datas

    # 获取专题中的 插画列表
    @classmethod
    def parse_illustration(cls, html):
        if not html:
            return None
        main = BeautifulSoup(html)
        datas = []
        title_data = HtmlDownloader.find_title_image(main)
        if title_data:
            datas.append(title_data)
        divs = main.findAll("div", attrs={"class": re.compile('am__work gtm__illust-collection-illusts-\d*')})
        # 适配某些专题页面
        if not divs:
            divs = main.findAll("div", attrs={"class": "am__work"})
        for div in divs:
            try:
                data = {}
                author_a = div.find("a", attrs={"class": "author-img-container inner-link"})
                title_a = div.find("h3", attrs={"class": "am__work__title"}).find("a")
                data["author"] = author_a.text
                data["author_page"] = author_a['href']
                data["title"] = title_a.text
                data["image_page"] = title_a["href"]
                image_img = div.find("img", attrs={"class": re.compile("am__work__illust\w*")})
                # 适配动图
                if not image_img:
                    image_img = div.find("img", attrs={"class": "ugoira-poster"})
                if image_img:
                    data["image"] = image_img["src"]
                else:
                    print(data["title"] + ":" + data[
                        "image_page"] + ":" + "can't find image。please use quality=1 mode download")
                data = parse_dict(data)
                datas.append(data)
            except Exception, e:
                print("Parse illustrations Warning:" + e.message)
                continue
        return datas

    # 用于标题展示的插画需要单独获取,某些专题没有该部分，忽视
    @classmethod
    def find_title_image(cls, main):
        try:
            aie_info = main.find("div", attrs={"class": "aie__icon-title-container"})
            data = {"image": aie_info.find("img", attrs={"class": "aie__uesr-icon"})["src"]}
            user_container = aie_info.find("div", attrs={"class": "aie__title-user-name-container"})
            image_a = user_container.find("p", attrs={"class": "aie__title"}).find("a")
            data["image_page"] = image_a['href']
            data["title"] = image_a.text
            user_a = user_container.find("p", attrs={"class": "aie__user-name"}).find("a")
            data["author_page"] = user_a["href"]
            data["author"] = user_a.text
            data = parse_dict(data)
            return data
        except Exception, e:
            print("Get topic Title Warning:" + e.message)
            return None
