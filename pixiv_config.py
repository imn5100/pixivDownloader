# -*- coding: utf-8 -*-

# 获取代理网页超时时间5s
TIMEOUT = 5
# 失败重试次数
RETRY_TIME = 3
# api请求头
HEADER = {
    'App-OS': 'ios',
    'App-OS-Version': '9.3.3',
    'App-Version': '6.0.9',
    'User-Agent': 'PixivIOSApp/6.0.9 (iOS 9.3.3; iPhone8,1)',
}
# 爬虫请求头
CRAWLER_HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # Pixivision 支持多语言，可以通过改变 Accept-Language  改变获取的插画专题描述语言。
    # ja  日文
    # zh 中文简体
    # zh-tw 中文繁体
    # en 或空或其他无法解析语言 英文
    'Accept-Language': 'zh',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Referer': 'http://www.pixivision.net'
}
# pixivision 网址
BASE_URL = "http://www.pixivision.net"
# 拉取插画专题 url
LINK_URL = "http://www.pixivision.net/en/c/illustration/?p=%s"
# illust detail url
ILLUST_DETAIL = "https://app-api.pixiv.net/v1/illust/detail"
ILLUST_RELATED = 'https://app-api.pixiv.net/v1/illust/related'
# redis set 过滤器相关设置
REDIS_IP = "127.0.0.1"
REDIS_PORT = 6379
REDIS_FILTER_KEY = "setFilter:Pixivision"
# 将存储空间分为三块 避免单set过大
BLOCK_NUM = 3

# Image quality  图片质量 1 最高级，使用api下载原图(找不到原图会下载大图，找不到大图下载展示图) 2 pixivision 展示用图
IMAGE_QUALITY = 1
# 存储插画的基本目录
IMAGE_SVAE_BASEPATH = "z_pixivision_download"
