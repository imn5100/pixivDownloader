# -*- coding: utf-8 -*-

# 获取代理网页超时时间5s
TIMEOUT = 5
# 失败重试次数
RETRY_TIME = 3
# 爬虫及api请求头
HEADER = {
    'App-OS': 'ios',
    'App-OS-Version': '9.3.3',
    'App-Version': '6.0.9',
    'User-Agent': 'PixivIOSApp/6.0.9 (iOS 9.3.3; iPhone8,1)',
}
# pixivision 网址
BASE_URL = "http://www.pixivision.net"
# illust detail url
ILLUST_DETAIL = "https://app-api.pixiv.net/v1/illust/detail"
ILLUST_RELATED = 'https://app-api.pixiv.net/v1/illust/related'
