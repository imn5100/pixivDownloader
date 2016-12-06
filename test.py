# -*- coding: utf-8 -*-
from pixiv_config import BASE_URL
from pixivapi.PixivApi import PixivApi
from pixivsion.PixivsionDownloader import HtmlDownloader, parse_illustration_list


def test_pixivsion():
    banner_list = parse_illustration_list(HtmlDownloader.download(BASE_URL))
    print(banner_list)
    print(banner_list[0].href)


def test_api():
    detail = PixivApi.illust_detail(54809586)
    print(detail.illust.meta_single_page.original_image_url)
    related = PixivApi.illust_related(54809586)
    print(related)


if __name__ == '__main__':
    test_pixivsion()
    test_api()
