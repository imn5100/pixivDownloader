# -*- coding: utf-8 -*-
import os
import threading
import time
from threading import Thread

from pixiv.PixivDataDownloader import PixivDataHandler
from pixiv.PixivHtmlParser import PixivHtmlParser
from pixiv_config import *
from pixivapi.AuthPixivApi import AuthPixivApi
from pixivapi.PixivApi import PixivApi
from pixivapi.PixivUtils import parse_dict, PixivError
from pixivision.PixivisionTopicDownloader import ImageDownload, IlluDownloadThread
from pixivision.PixivisionHtmlParser import HtmlDownloader
from utils import CommonUtils, LoggerUtil


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
    detail = PixivApi.illust_detail(52819443)
    print(detail.illust)
    # related = PixivApi.illust_related(54809586)
    # print(related)


def test_image_download():
    topics = ImageDownload.get_pixivision_topics("http://www.pixivision.net/en/c/illustration/?p=2",
                                                 IMAGE_SAVE_BASEPATH)
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
    api = AuthPixivApi("", "", access_token='dQ63rSzFSIpvbbkAJnV41xrRv3evYy_nXcLEUaobku8')
    # obj = api.search_works("艦これ")
    # print(obj)
    # print (api.illust_detail(52819443))
    # print (api.works(39562690))
    # print (api.spotlight(category='illust'))
    # print (api.illust_related(59252176))
    # print (api.search_works('百合'))
    # print (api.search_illust('百合'))
    return api.search_popular_illust('百合', offset=None)
    # print (api.app_ranking(date='2017-07-11'))
    # print (api.ranking())
    # print (api.illust_recommended())


def download_test(url):
    print("start download:" + str(time.time()))
    PixivApi.download(url)
    # 取最终一个url下载结束时间
    print("url:" + url + " end:" + str(time.time()))


def download_thread_test():
    urls = ["https://i4.pixiv.net/img-original/img/2016/09/13/12/23/34/58959975_p0.jpg",
            "https://i1.pixiv.net/img-original/img/2015/12/27/22/22/00/54279980_p0.jpg",
            "https://i1.pixiv.net/img-original/img/2014/05/28/01/21/50/43748656_p0.jpg",
            "https://i1.pixiv.net/img-original/img/2016/08/20/00/16/23/58541644_p0.png"]
    ts = []
    for url in urls:
        t = Thread(target=download_test, args=(url,))
        t.daemon = True
        t.start()
        ts.append(t)
    for t in ts:
        t.join()


def test_html_parse_byfile_for_search():
    html = open("test.html").read()
    search_result = PixivHtmlParser.parse_search_result(html)
    pop_result = PixivHtmlParser.parse_popular_introduction(html)
    print(search_result)
    print(pop_result)


def testbs4():
    from bs4 import BeautifulSoup
    import re
    html = open("test.html").read()
    soup = BeautifulSoup(html)
    lis = soup.find_all("li", class_=re.compile("image-item\s*"))
    datas = []
    for li in lis:
        try:
            url = li.find_all("a", class_=re.compile("work _work\s*"))
            print(url[0])
            data = {"url": PIXIV_URL + li.find_all("a", class_=re.compile("work  _work\w*"), limit=1)[0]['href'],
                    "title": li.find("h1", attrs={"class": "title"}).text}
            # 非关键信息 解析失败不影响主要信息收集
            try:
                user = {}
                user_a = li.find("a", attrs={"class": "user ui-profile-popup"})
                user["name"] = user_a["title"]
                user["id"] = user_a["data-user_id"]
                user["page"] = PIXIV_URL + user_a["href"]
                data["user"] = user
            except Exception as e:
                print("Parse User Warning")
                print(e.message)
            count_a = li.find("a", attrs={"class": "bookmark-count _ui-tooltip"})
            if count_a:
                data["mark_count"] = li.find("a", attrs={"class": "bookmark-count _ui-tooltip"}).text
            else:
                data["mark_count"] = 0
            data = parse_dict(data)
            datas.append(data)
        except Exception as e:
            print("parse_search_result Warning")
            print(e.message)
            continue
    return datas


def test_str_find():
    data = {'title': u'想抱着睡觉♡抱枕套风格的插画特辑', 'size': '15',
            'description': u'印着角色躺在上面的图的抱枕套，在宅向周边里一直都特别受欢迎。将抱枕放在床上，仿佛最喜爱的那个角色就睡在自己身边一样，有时候还会兴奋到无法安睡。而抱着抱枕酣然入睡的时候，又会做一个怎样的美梦呢？这次，就为大家送上描绘了“抱枕套”的插画作品特辑。快来看看吧！',
            'url': 'https://www.pixivision.net/zh/a/2613'}
    file_path = "/Users/imn5100/Downloads/pixiv/想抱着睡觉♡抱枕套风格的插画特辑//topic.txt"
    CommonUtils.write_topic_des(file_path, data)


def api_search(keyword, api, page=1, download_threshold=DOWNLOAD_THRESHOLD):
    illusts = []
    if CommonUtils.is_empty(keyword):
        raise PixivError('[ERROR] keyword is empty')
    ids = set()
    count = 0
    for data in api.search_popular_illust('百合').illusts:
        if download_threshold:
            if data.total_bookmarks >= download_threshold:
                if data.id not in ids:
                    ids.add(data.id)
                    illusts.append(data)
        elif data.id not in ids:
            ids.add(data.id)
            illusts.append(data)
    if page:
        while page > 0:
            for data in api.search_illust('百合', offset=count).illusts:
                count = count + 1
                if download_threshold:
                    if data.total_bookmarks >= download_threshold:
                        if data.id not in ids:
                            ids.add(data.id)
                            illusts.append(data)
                elif data.id not in ids:
                    ids.add(data.id)
                    illusts.append(data)
            page = page - 1
    return illusts


def testPage_search():
    handler = PixivDataHandler('', '',
                               cookies={'device_token': '7faf9c841824ca3411def80c0fb29631', 'p_ab_id': '5',
                                        'PHPSESSID': '', 'p_ab_id_2': '9'})
    urls = set()
    for page in range(1, 7):
        for data in handler.search(u'百合', page=page, download_threshold=200):
            urls.add(data.url)
    print (len(urls))


proxy = {
    'ip': '127.0.0.1',
    'port': '1080'
}
proxies = {
    "https": r"socks5://%s:%s" % (proxy['ip'], proxy['port']),
    "http": r"socks5://%s:%s" % (proxy['ip'], proxy['port'])
}


def test_proxy_by_requesocks():
    import requesocks as requests

    session = requests.session()
    session.proxies = proxies
    m = session.get('https://pixiv.net', headers=PIXIV_PAGE_HEADERS)
    print (m.content)


def test_proxy_by_urllib2():
    import urllib2
    import socks
    from sockshandler import SocksiPyHandler
    headers = {'Host': 'app-api.pixiv.net', 'User-Agent': 'PixivIOSApp/6.0.9', 'Accept-Language': 'zh',
               'Authorization': 'Bearer %s' % 'uMzgoLH6TysDAvu8594IvustucSHz0hwThlMYG3uHY0', 'Accept-Encoding': 'gzip'}
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=1)

    opener = urllib2.build_opener(httpHandler, httpsHandler, SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 1080))
    urllib2.install_opener(opener)

    req = urllib2.Request("https://app-api.pixiv.net/v1/illust/detail?illust_id=55418",
                          headers=headers)
    x = urllib2.urlopen(req)
    print (x.read())


def unzip(data):
    import gzip
    import StringIO
    data = StringIO.StringIO(data)
    gz = gzip.GzipFile(fileobj=data)
    data = gz.read()
    gz.close()
    return data


def test_relate():
    api = AuthPixivApi(None, None, access_token='')
    result = api.illust_related(67874620)
    next_url = result.next_url
    datas = result.illusts
    print(next_url)
    print(datas)


def test_thread():
    worker = Thread(target=lambda: LoggerUtil.error_log(threading.currentThread().getName()), name='worker' + str(1))
    worker.start()


if __name__ == '__main__':
    test_thread()
