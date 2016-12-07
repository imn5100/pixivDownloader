# -*- coding: utf-8 -*-

import redis

from pixiv_config import *
from pixivapi.PixivApi import PixivApi
from pixivsion.ImageDownload import ImageDownload, IlluDownloadThread
from pixivsion.PixivisionDownloader import HtmlDownloader
from utils.RedisFilter import RedisFilter


def test_pixivsion():
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
    topics = ImageDownload.get_pixivision_topics("http://www.pixivision.net/en/c/illustration/?p=2", IMAGE_SVAE_BASEPATH)
    ts = []
    for topic in topics:
        t = IlluDownloadThread(topic.href, topic.save_path, 1)
        t.start()
        ts.append(t)
    for t in ts:
        t.join()


def test_html_parse_byfile():
    html = open("test.html").read()
    print(HtmlDownloader.parse_illustration(html))


if __name__ == '__main__':
    test_image_download()
