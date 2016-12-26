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
ILLUST_DETAIL_PAGE = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s"
# Pixivision全站总页数,用于全站爬取 2016/12/12
PAGE_NUM = 62
# illust detail url
ILLUST_DETAIL = "https://app-api.pixiv.net/v1/illust/detail"
ILLUST_RELATED = 'https://app-api.pixiv.net/v1/illust/related'
# redis set 过滤器相关设置
REDIS_IP = "127.0.0.1"
REDIS_PORT = 6379
REDIS_FILTER_KEY = "setFilter:Pixivision"
# 将存储空间分为三块 避免单set过大
BLOCK_NUM = 3
USE_FILTER = False
# 是否覆盖已下载的插画,False 时，已下载的插画会跳过下载，True时，无论插画是否存在，都会下载，并覆盖原文件
OVERRIDE_IMAGE = False
# Image quality  图片质量 1 最高级，使用api下载原图(找不到原图会下载大图，找不到大图下载展示图) 2 pixivision 展示用图(大小和画质都有压缩)
IMAGE_QUALITY = 1
# 存储插画的基本目录
IMAGE_SVAE_BASEPATH = "E:/imageDownLoad/z_pixivision_download"
# 文件命名是否使用原文件名（即插画作者的命名）
# 因为插画原名经常出现颜文字和各种奇怪的符号，这里不使用图片标题进行命名，用pixiv 的id进行命名会很大地减少文件错误，提高下载正确率，
# 缺点是 会丢失原文件名字。
IMAGE_USE_ORG_NAME = True

#################################################
# 以下为pixiv主站网页请求相关配置
# model in (daily,weekly,male,female)
# p is Page index
RANKING_URL = "http://www.pixiv.net/ranking.php?format=json&mode=%s&p=%d"
# p站网址
PIXIV_URL = "http://www.pixiv.net"
# pixiv 页面请求请求头
PIXIV_PAGE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'accounts.pixiv.net',
    'Referer': 'http://www.pixiv.net/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'
}
# 关键字搜索页面search  page type in(illust,ugoira,manga) &scd=2016-11-26&order=date
PIXIV_SEARCH_URL = "http://www.pixiv.net/search.php?word=%s&type=%s&p=%d"
PIXIV_LOGIN_KEY = "https://accounts.pixiv.net/login"
PIXIV_LOGIN_URL = "https://accounts.pixiv.net/api/login"
# 下载阈值、收藏数>THRESHOLD 才进行下载
DOWNLOAD_THRESHOLD = 100

