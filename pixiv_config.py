# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils.Config import Config

# 通过项目外的配置文件获取配置(避免更新项目代码时配置也被覆盖)。不想配置文件可以直接在config.get中的default_value填写自己的配置。
# 配置文件例子config.ini，放置位置：本项目所在文件夹
config = Config('../config.ini', "pixiv")

# *****************************                      重要配置                         ******************************
# *****************************除图形界面下载器以外 (账号+密码) 或 (Access token) 必填一项 否者无法拉取插画详情 ******************************
# Pixiv账户 和 密码
USERNAME = config.get("USERNAME", default_value="*")
PASSWORD = config.get("PASSWORD", default_value="*")
# 访问pixiv api的凭证，使用账户密码登录后获得,可重复使用，不需要每次都用账号密码登录。
ACCESS_TOKEN = config.get("ACCESS_TOKEN", default_value="")
# 刷新token token失效后，使用refresh  token 刷新，可获得新token
REFRESH_TOKEN = config.get("REFRESH_TOKEN", default_value="3W1T_8NmOun_RISbqjx8jkV2Eo2vdtUde-")
# *****************************  cookie 用于记录网页登录状态。使用搜索功能时：(账号+密码) 或 (Cookie) 必填一项
# 如果不想反复登录，可以在第一次登陆后，从控制台获取输出的cookie信息。配置于此。（反复重复登陆 除了会收到Pixiv寄出的安全提示邮件外暂无其他影响）
# 不使用cookies 请保持默认值为"{}"
PIXIV_COOKIES = eval(config.get("PIXIV_COOKIES",
                                default_value="{}"))

# 获取代理网页超时时间5s
TIMEOUT = config.getint("TIMEOUT", default_value=5)
# 失败重试次数
RETRY_TIME = config.getint("RETRY_TIME", default_value=3)
# api请求头
HEADER = {
    'App-OS': 'ios',
    'App-OS-Version': '9.3.3',
    'App-Version': '6.8.3',
    'User-Agent': 'PixivIOSApp/6.8.3 (iOS 9.3.3; iPhone8,1)',
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
# Pixivision全站总页数,用于全站爬取 2017/5/24
# 全站爬取完毕后，如果Pixivsion有更新，可以修改此配置，比如Pixivsion有2页更新未爬取，修改PAGE_NUM=2,全站插画爬虫则会爬取前2页的所有特辑
PAGE_NUM = config.getint("PAGE_NUM", default_value=77)
# illust detail url
ILLUST_DETAIL = "https://app-api.pixiv.net/v1/illust/detail"
ILLUST_RELATED = 'https://app-api.pixiv.net/v2/illust/related'
# 是否覆盖已下载的插画,False 时，已下载的插画会跳过下载，True时，无论插画是否存在，都会下载，并覆盖原文件
OVERRIDE_IMAGE = config.getboolean("OVERRIDE_IMAGE", default_value=False)
# 存储插画的基本目录
IMAGE_SAVE_BASEPATH = config.getint("IMAGE_SAVE_BASEPATH",
                                    default_value=' /Users/imn5100/Downloads/pixiv/z_pixivision_download')
# 文件命名是否使用原文件名（即插画作者的命名）
# 因为插画原名经常出现颜文字和各种奇怪的符号，这里不使用图片标题进行命名，用pixiv 的id进行命名会很大地减少文件错误，提高下载正确率，
# 缺点是 会丢失原文件名字。
# 弃用配置 文件命名仅支持 pixiv id,方便查询作品详情，追溯作者。
# IMAGE_USE_ORG_NAME = False

####################################
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
PIXIV_SEARCH_URL = "https://www.pixiv.net/search.php?word=%s&type=%s&p=%d"
PIXIV_LOGIN_KEY = "https://accounts.pixiv.net/login"
PIXIV_LOGIN_URL = "https://accounts.pixiv.net/api/login"
#######################################
# 下载设置
# 下载阈值、收藏数>THRESHOLD 才进行下载
DOWNLOAD_THRESHOLD = config.getint("DOWNLOAD_THRESHOLD", default_value=200)
# 多图作品限制P数，多p插画 大于 P_LIMIT 张跳过下载。有些插画太多了，严重影响整体下载速度。
P_LIMIT = config.getint("P_LIMIT", default_value=10)
# 搜索页数
SEARCH_PAGE = config.getint("SEARCH_PAGE", default_value=2)
# 存储位置 必须为有效路径否则会报错
SEARCH_SAVE_PATH = config.get("SEARCH_SAVE_PATH", default_value="/Users/imn5100/Downloads/pixiv/search")
# 搜索关键字
SEARCH_KEYWORD = config.get("SEARCH_KEYWORD", default_value="夕立")
# 是否检查文件下载完整 需要安装 pillow
CHECK_IMAGE_VERIFY = config.getboolean("CHECK_IMAGE_VERIFY", default_value=True)
