# -*- coding: utf-8 -*-
import getpass
from Queue import Queue
from threading import Thread

from pixiv import PixivDataDownloader
from pixiv.PixivImageDownloader import download_queue
from pixivapi.AuthPixivApi import AuthPixivApi
from pixiv_config import USERNAME, PASSWORD, DOWNLOAD_THRESHOLD, SEARCH_KEYWORD, SEARCH_PAGE, SEARCH_SAVE_PATH

if __name__ == '__main__':
    type = raw_input("Please chose run mode.1.Use pixiv_config file to search. 2. Enter the parameters manually:\n")
    if type == "1":
        username = USERNAME
        password = PASSWORD
        data_handler = PixivDataDownloader.PixivDataHandler(username, password)
        auth_api = AuthPixivApi(username, password)
        print("Login success!!!!")
        download_threshold = DOWNLOAD_THRESHOLD
        path = SEARCH_SAVE_PATH
        page = SEARCH_PAGE
        keyword = SEARCH_KEYWORD
    else:
        username = raw_input("Please enter your pixiv accounts eamil or pixiv ID\n")
        password = getpass.getpass('Enter password:\n ')
        data_handler = PixivDataDownloader.PixivDataHandler(username, password)
        auth_api = AuthPixivApi(username, password)
        print("Login success!!!!")
        path = raw_input("Please input illustration save path:\n")
        page = int(raw_input("Please enter the total number of pages you want to crawl:\n"))
        download_threshold = int(raw_input("Please enter the minimum number of illustration's bookmarks:\n"))
        keyword = raw_input("Please enter search keyword:\n")
    queue = Queue()
    thread_num = page if page <= 30 else 30
    for i in range(thread_num):
        t = Thread(target=download_queue, args=(queue, path, auth_api))
        t.daemon = True
        t.start()
    for p in range(1, page + 1):
        result = data_handler.search(keyword, page=p, download_threshold=download_threshold)
        print(result)
        queue.put(result)
    queue.join()
