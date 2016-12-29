# -*- coding: utf-8 -*-

import redis
import time

from pixiv.PixivPageDownloader import PixivHtmlParser
from pixiv_config import *
from pixivapi.AuthPixivApi import AuthPixivApi
from pixivapi.PixivApi import PixivApi
from pixivision.ImageDownload import ImageDownload, IlluDownloadThread
from pixivision.PixivisionDownloader import HtmlDownloader
from utils.RedisFilter import RedisFilter


def test_pixivision():
    topic_list = HtmlDownloader.parse_illustration_topic(
            HtmlDownloader.download("http://www.pixivision.net/en/c/illustration/?p=1"))
    for topic in topic_list:
        print(topic)
    # 创建特辑文件夹，写入特辑信息。
    href = topic_list[0].href
    illu_list = HtmlDownloader.parse_illustration(HtmlDownloader.download(href))
    for illu in illu_list:
        print(illu)


def test_api():
    detail = PixivApi.illust_detail(54809586)
    print(detail.illust)
    related = PixivApi.illust_related(54809586)
    print(related)


def test_redisFilter():
    r = redis.Redis(REDIS_IP, REDIS_PORT)
    rFilter = RedisFilter(r, 3, "setFilter:Pixivision")
    datas = ["/zh/c/1001", "/zh/c/1002", "/zh/c/1003", "/zh/c/1004", "/zh/c/1005", "/zh/c/1006", "/zh/c/1008",
             "/zh/c/1009"]
    other = "/zh/c/1007"
    rFilter.add_all(datas)
    print(rFilter.is_contained(datas[2]))
    print(rFilter.is_contained(other))
    rFilter.add(other)
    print(rFilter.is_contained(other))
    rFilter.remove(datas[1])
    print(rFilter.is_contained(datas[1]))
    rFilter.remove_all(datas)
    rFilter.remove(other)
    print(rFilter.is_contained(datas[2]))


def test_image_download():
    topics = ImageDownload.get_pixivision_topics("http://www.pixivision.net/en/c/illustration/?p=2",
                                                 IMAGE_SVAE_BASEPATH)
    ts = []
    for topic in topics:
        t = IlluDownloadThread(topic.href, topic.save_path, 1)
        t.start()
        ts.append(t)
    for t in ts:
        t.join()


def test_html_parse_byfile():
    html = open("test.html").read()
    print(HtmlDownloader.get_title(html))


def test_pixiv_html_parse_byfile():
    html = open("test.html").read()
    search_result = PixivHtmlParser.parse_search_result(html)
    pop_result = PixivHtmlParser.parse_popular_introduction(html)
    print(search_result)
    print(len(search_result))
    print(pop_result)
    print(len(pop_result))
    print("normal result after filter：")
    search_result = filter(lambda data: data.has_key("mark_count") and int(data.mark_count) > 1000, search_result)
    print(search_result)
    print(len(search_result))


def test_auth_api():
    api = AuthPixivApi("*", "*", access_token="qC-MDpoHtD3ZuN24Ow5LLD-4H3Phs0YtB0S9Dn-E8L0")
    obj = api.search_works("艦これ")
    print(obj)
    resp_page = api.auth_requests_call("get", "http://www.pixiv.net/search.php?word=艦これ&type=illust")
    print(resp_page.content)


if __name__ == '__main__':
    start = time.time()
    PixivApi.download("http://i3.pixiv.net/img-original/img/2016/12/24/01/00/01/60514190_p0.png")
    print ((time.time() - start) * 1000)
