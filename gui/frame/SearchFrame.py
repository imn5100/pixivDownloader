# -*- coding: utf-8 -*-
from Tkinter import *
from threading import Thread
from tkMessageBox import showwarning, showerror, showinfo

import os

from gui.DownloadTask import TASK_TYPE_SEARCH_API, TASK_TYPE_SEARCH, Task, DOWNLOAD_MODE_ID, DOWNLOAD_MODE_DETAIL
from gui.frame.PixivFrame import PixivFrame
from pixiv_config import DOWNLOAD_THRESHOLD, IMAGE_SAVE_BASEPATH
from pixivapi.PixivUtils import PixivError
from utils import CommonUtils, AtomicInteger


class SearchFrame(PixivFrame):
    def __init__(self, master, name, queue, api, search_handler):
        PixivFrame.__init__(self, master, name)
        self.search_handler = search_handler
        self.api = api
        self.queue = queue
        self.keywords = StringVar(value='1000users入り')
        self.page_number = StringVar(value=2)
        self.fav_num = StringVar(value=500)
        self.p_limit = StringVar(value=10)
        self.path_var = StringVar(value=IMAGE_SAVE_BASEPATH)

    def init_ui(self):
        self.init_search()

    def init_search(self):
        # search组件
        keywords_label = Label(self, text="Key Words:", width=57, height=1)
        keywords_label.pack()

        keywords_entry = Entry(self, width=57, textvariable=self.keywords)
        keywords_entry.pack()

        search_path_label = Label(self, text="Download Path:", width=30, height=1)
        search_path_label.pack()

        search_path_entry = Entry(self, width=57, textvariable=self.path_var)
        search_path_entry.pack()

        fav_num_label = Label(self, text="Minimum number of favorites:", width=30, height=1)
        fav_num_label.pack()

        fav_num_entry = Entry(self, width=57, textvariable=self.fav_num)
        fav_num_entry.pack()

        page_label = Label(self, text="Number of pages:", width=30, height=1)
        page_label.pack()

        page_entry = Entry(self, width=57, textvariable=self.page_number)
        page_entry.pack()

        p_limit_label = Label(self, text="Single works P limit(0 means no Limit):", width=30, height=1)
        p_limit_label.pack()

        p_limit_entry = Entry(self, width=57, textvariable=self.p_limit)
        p_limit_entry.pack()

        search_button = Button(self, text='Start', height=2, command=self.handle_search)
        search_button.pack()

    def handle_search(self):
        keywords = self.keywords.get().strip()
        if CommonUtils.is_empty(keywords):
            showwarning("warning", "Please enter search keywords!")
            print ("warning", "Please enter search keywords!")
            return
        if CommonUtils.is_empty(self.path_var.get()):
            showwarning("warning", "path can't be empty!")
            print ("warning", "path can't be empty!")
            return
        path = self.path_var.get().strip()
        if not os.path.exists(path):
            showerror("error", " No such file or directory!")
            print ('error', 'No such file or directory')
            return
        path = path + "/" + CommonUtils.filter_dir_name("search_" + keywords)
        showinfo("info", "Is searching：")
        search_handler = Thread(target=self.search, args=(keywords, path))
        search_handler.start()

    def search(self, keywords, path):
        id_set = set()
        page = CommonUtils.set_int(self.page_number.get(), 2)
        fav_num = CommonUtils.set_int(self.fav_num.get(), 0)
        tasks = []
        for p in range(1, page + 1):
            result = self.search_handler.search(keywords, page=p,
                                                download_threshold=fav_num)
            if len(result) == 0:
                print ('warning', 'Page:' + str(p) + ' Search  results are Empty')
                continue
            for illu in result:
                if illu.id in id_set:
                    continue
                else:
                    task = Task(TASK_TYPE_SEARCH, DOWNLOAD_MODE_ID, title='search '+keywords, path=path,
                                p_limit=CommonUtils.set_int(self.p_limit.get(), 0), id=illu.id, illu=illu,
                                get_from='search_page')
                    id_set.add(illu.id)
                    tasks.append(task)
        print ('Search ' + keywords + ' from web page get:' + str(len(tasks)))
        api_search_data = api_search(keywords, self.api, page=page, download_threshold=fav_num, id_set=id_set)
        if len(api_search_data) == 0:
            print ('warning', 'Api search results are empty')
        else:
            print ('Search ' + keywords + ' from pixiv Api get:' + str(len(api_search_data)))
            for illu in api_search_data:
                task = Task(TASK_TYPE_SEARCH_API, DOWNLOAD_MODE_DETAIL, path=path,
                            p_limit=CommonUtils.set_int(self.p_limit.get(), 0),
                            illu=illu, title='search '+keywords, get_from='search_api')
                tasks.append(task)
        all_count = len(tasks)
        if all_count > 0:
            current_count = AtomicInteger.AtomicInteger()
            if not os.path.exists(path):
                os.makedirs(path)
            for task in tasks:
                task.all_count = all_count
                task.current_count = current_count
                self.queue.add_work(task)


def api_search(keyword, api, page=1, download_threshold=DOWNLOAD_THRESHOLD, id_set=None):
    illusts = []
    if CommonUtils.is_empty(keyword):
        raise PixivError('[ERROR] keyword is empty')
    if id_set:
        ids = id_set
    else:
        ids = set()
    count = 0
    for data in api.search_popular_illust(keyword).illusts:
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
            for data in api.search_illust(keyword, offset=count).illusts:
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
