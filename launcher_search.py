# -*- coding: utf-8 -*-
import os
from Queue import Queue
from threading import Thread

from pixiv import PixivDataDownloader
from pixiv.PixivImageDownloader import download_queue
from pixiv_config import USERNAME, PASSWORD, DOWNLOAD_THRESHOLD, SEARCH_KEYWORD, SEARCH_PAGE, SEARCH_SAVE_PATH, \
    PIXIV_COOKIES
from pixivapi.AuthPixivApi import AuthPixivApi
from pixivapi.PixivApi import PixivApi
from utils import CommonUtils

if __name__ == '__main__':
    type = raw_input("Please chose run mode.1.Use pixiv_config file to search. 2. Enter the parameters manually:\n")
    if type == "1":
        username = USERNAME
        password = PASSWORD
        print ("Loading")
        # PixivDataDownloader.PixivDataHandler() 也可以不登陆进行数据爬取，但不登陆就没有人气推荐作品。爬取的插画质量会低很多，所以干脆强制要求登录了。
        if len(PIXIV_COOKIES) >= 3:
            data_handler = PixivDataDownloader.PixivDataHandler(cookies=PIXIV_COOKIES)
        else:
            data_handler = PixivDataDownloader.PixivDataHandler(username, password)
        # 这里可以使用两种api进行下载， AuthPixivApi和PixivApi 。 AuthPixivApi需要登录，但能下载更多限制级别的插画。通常情况PixivApi即可满足需求。
        auth_api = PixivApi()
        print("Login success!!!!")
        download_threshold = DOWNLOAD_THRESHOLD
        path = SEARCH_SAVE_PATH
        page = SEARCH_PAGE
        keyword = SEARCH_KEYWORD
    else:
        username = raw_input("Please enter your pixiv accounts eamil or pixiv ID\n")
        password = raw_input('Enter password:\n ')
        print ("Loading")
        data_handler = PixivDataDownloader.PixivDataHandler(username, password)
        auth_api = AuthPixivApi(username, password)
        print("Login success!!!!")
        path = raw_input("Please input illustration save path:\n")
        page = int(raw_input("Please enter the total number of pages you want to crawl:\n"))
        download_threshold = int(raw_input("Please enter the minimum number of illustration's bookmarks:\n"))
        keyword = raw_input("Please enter search keyword:\n")
        keyword = keyword.decode("utf-8")
    queue = Queue()
    path = path + "/" + CommonUtils.filter_dir_name("search_" + keyword)
    # 默认消费者下载线程数为10个，可根据下载量和机器性能适当增加
    thread_num = 10
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(thread_num):
        t = Thread(target=download_queue, name="Thread" + str(i), args=(queue, path, auth_api))
        t.daemon = True
        t.start()
    # 因为搜索的结果量不大，直接使用set在内存中过滤重复元素，不需要使用redisFilter
    set_filter = set()
    for p in range(1, page + 1):
        result = data_handler.search(keyword, page=p, download_threshold=download_threshold)
        print(result)

        for illu in result:
            if illu.url in set_filter:
                continue
            else:
                # 拆分插画列表放入队列，减少任务分配不均的概率
                queue.put(illu)
                # 放入队列成功后才能放入set
                set_filter.add(illu.url)
    # 等待队列任务完成
    queue.join()
