# -*- coding: utf-8 -*-
import redis

from pixiv_config import *
from pixivapi.PixivApi import PixivApi
from pixivsion.PixivsionDownloader import HtmlDownloader
from utils.RedisFilter import RedisFilter


def test_pixivsion():
    banner_list = HtmlDownloader.parse_illustration_list(HtmlDownloader.download(BASE_URL))
    print(banner_list)
    print(banner_list[0].href)


def test_api():
    detail = PixivApi.illust_detail(54809586)
    print(detail.illust.meta_single_page.original_image_url)
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


if __name__ == '__main__':
    test_redisFilter()
