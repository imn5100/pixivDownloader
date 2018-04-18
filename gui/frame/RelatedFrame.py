# -*- coding: utf-8 -*-
import os
from Tkinter import *
from threading import Thread
from tkMessageBox import showwarning, showerror, showinfo

from gui.DownloadTask import Task, DOWNLOAD_MODE_DETAIL, TASK_TYPE_RELATED
from gui.frame.PixivFrame import PixivFrame
from pixiv_config import IMAGE_SAVE_BASEPATH
from utils import CommonUtils, AtomicInteger


class RelatedFrame(PixivFrame):
    def __init__(self, master, name, queue, api):
        PixivFrame.__init__(self, master, name)
        self.api = api
        self.queue = queue
        self.id_var = StringVar()
        self.page_number = StringVar(value=2)
        self.fav_num = StringVar(value=500)
        self.p_limit = StringVar(value=10)
        self.path_var = StringVar(value=IMAGE_SAVE_BASEPATH)

    def init_ui(self):
        self.init_related()

    def init_related(self):
        # 关联下载组件
        keywords_label = Label(self, text="Related Seed Id:", width=57, height=1)
        keywords_label.pack()

        keywords_entry = Entry(self, width=57, textvariable=self.id_var)
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

        search_button = Button(self, text='Start', height=2, command=self.handle_related)
        search_button.pack()

    def handle_related(self):
        id_var = CommonUtils.set_int(self.id_var.get().strip())
        if id_var <= 0:
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
        path = path + "/" + CommonUtils.filter_dir_name("related_" + str(id_var))
        showinfo("info", "Get related illus of " + str(id_var) + " :")
        related_handler = Thread(target=self.related, args=(id_var, path))
        related_handler.start()

    def related(self, id_var, path):
        page = CommonUtils.set_int(self.page_number.get(), 2)
        fav_num = CommonUtils.set_int(self.fav_num.get(), 0)
        illusts = []
        result = self.api.illust_related(id_var)
        next_url = result.next_url
        datas = result.illusts
        if len(datas) == 0:
            print ('warning', 'Get related illus of' + str(id_var) + ' are empty')
            return
        illusts.extend(datas)
        page -= 1
        while len(datas) > 0 and CommonUtils.is_not_empty(next_url) and page > 0:
            result = self.api.get(next_url)
            datas = result.illusts
            next_url = result.next_url
            illusts.extend(datas)
            page -= 1

        tasks = []
        id_set = set()
        p_limit = CommonUtils.set_int(self.p_limit.get(), 0)
        for illust in illusts:
            if not illust or illust.id in id_set:
                continue
            if fav_num > 0:
                if illust.total_bookmarks < fav_num:
                    continue
            task = Task(TASK_TYPE_RELATED, DOWNLOAD_MODE_DETAIL, path=path, p_limit=p_limit, illu=illust,
                        title="related by id " + str(id_var), get_from='related')
            tasks.append(task)
            id_set.add(illust.id)
        if len(tasks) == 0:
            print ('warning', 'Get related illus of ' + str(id_var) + ' are empty')
            return
        else:
            print ('Get related illus of' + str(id_var) + ' All:' + str(len(tasks)))
        all_count = len(tasks)
        current_count = AtomicInteger.AtomicInteger()
        if not os.path.exists(path):
            os.makedirs(path)
        for task in tasks:
            task.all_count = all_count
            task.current_count = current_count
            self.queue.add_work(task)
