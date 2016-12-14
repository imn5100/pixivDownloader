# -*- coding: utf-8 -*-

import redis
import time
from BeautifulSoup import BeautifulSoup

from pixiv_config import *
from pixivapi.PixivApi import PixivApi
from pixivapi.PixivUtils import parse_json
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
    rFilter = RedisFilter(r)
    datas = ["/zh/c/1001", "/zh/c/1002", "/zh/c/1003", "/zh/c/1004", "/zh/c/1005", "/zh/c/1006", "/zh/c/1008",
             "/zh/c/1009"]
    other = "/zh/c/1007"
    rFilter.add_all(datas)
    print(rFilter.is_contained(datas[2]))
    print(rFilter.is_contained(other))
    rFilter.add(other)
    print(rFilter.is_contained(other))
    rFilter.remove_all(datas)
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


def test_relate_illust():
    related = PixivApi.illust_related(54809586)
    print(len(related.illusts))
    print(related.next_url)
    url = related.next_url
    count = 1
    while True:
        # 间隔时间
        time.sleep(2)
        resp = HtmlDownloader.download(url)
        related2 = parse_json(resp)
        url = related2.next_url
        print("Depth :" + str(count) + " Associated illust:" + str(len(related2.illusts)))
        print("Next URL:" + related2.next_url)
        # 需要到达的深度
        if count == 10:
            break
        count += 1


if __name__ == '__main__':
    test_relate_illust()
