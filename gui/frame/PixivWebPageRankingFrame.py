# -*- coding: utf-8 -*-
import datetime
import os
import time
from Tkinter import *
from threading import Thread
from tkMessageBox import showwarning, showerror, showinfo

from tkinter import ttk

from gui.DownloadTask import Task, TASK_TYPE_RANKING, DOWNLOAD_MODE_ID
from gui.frame.PixivFrame import PixivFrame
from pixiv_config import IMAGE_SAVE_BASEPATH
from utils import CommonUtils, AtomicInteger

# pixiv page ranking mode
page_ranking_mode = (
    'daily', 'weekly', 'monthly', 'rookie', 'original', 'male', 'female',
    # r18
    'male_r18', 'female_r18', 'weekly_r18', 'daily_r18'
)


class PixivWebPageRankingFrame(PixivFrame):
    def __init__(self, master, name, queue, pixiv_data_handler):
        PixivFrame.__init__(self, master, name)
        self.queue = queue
        self.pixiv_data_handler = pixiv_data_handler
        self.p_limit = StringVar(value=10)
        self.path_var = StringVar(value=IMAGE_SAVE_BASEPATH)
        self.mode_var = StringVar(value='daily')
        #  %H:%M:%S
        self.date_var = StringVar(
            value=time.strftime("%Y-%m-%d", (datetime.datetime.now() - datetime.timedelta(days=1)).timetuple()))

    def init_ui(self):
        self.init_ranking()

    def init_ranking(self):
        # ranking 组件
        mode_label = Label(self, text="Mode:", width=57, height=1)
        mode_label.pack()

        mode_box = ttk.Combobox(self, width=20, textvariable=self.mode_var, state='readonly')
        mode_box['values'] = page_ranking_mode
        mode_box.pack()
        mode_box.focus_displayof()

        date_label = Label(self, text="Ranking Date:", width=10, height=1)
        date_label.pack()

        date_entry = Entry(self, width=20, textvariable=self.date_var)
        date_entry.pack()

        page_label = Label(self, text="Number of pages:", width=30, height=1)
        page_label.pack()

        p_limit_label = Label(self, text="Single works P limit(0 does not limit):", width=30, height=1)
        p_limit_label.pack()

        p_limit_entry = Entry(self, width=57, textvariable=self.p_limit)
        p_limit_entry.pack()

        ranking_path_label = Label(self, text="Download Path:", width=30, height=1)
        ranking_path_label.pack()

        ranking_path_entry = Entry(self, width=57, textvariable=self.path_var)
        ranking_path_entry.pack()

        ranking_button = Button(self, text='Start', height=2, command=self.handle_ranking)
        ranking_button.pack()

    def handle_ranking(self):
        mode = self.mode_var.get()
        path = self.path_var.get().strip()
        date = self.date_var.get().strip()
        if CommonUtils.is_empty(path):
            showwarning("warning", "path can't be empty!")
            print ("warning", "path can't be empty!")
            return
        if not os.path.exists(path):
            showerror("error", " No such file or directory!")
            print ('error', 'No such file or directory')
            return
        if not CommonUtils.validate_date_str(date):
            showerror("error", "Date Wrong!")
            print ('error', 'Date Wrong')
            return
        if datetime.datetime.strptime(date, '%Y-%m-%d') > datetime.datetime.now():
            showerror("error", "The date can not be greater than the day!")
            print ('error', 'The date can not be greater than the day')
            return
        showinfo("info", "Get ranking...")
        ranking_handler = Thread(target=self.ranking, args=(path, mode, date))
        ranking_handler.start()

    def ranking(self, path, mode, date):
        path = path + "/ranking_" + mode + '_' + date
        tasks = []
        if mode:
            ranking_data = self.pixiv_data_handler.ranking(mode, date.replace('-', ''))
            if len(ranking_data) > 0:
                print ('Get from pixiv web page ranking:' + str(len(ranking_data)))
                for illu in ranking_data:
                    task = Task(TASK_TYPE_RANKING, DOWNLOAD_MODE_ID, path=path,
                                p_limit=CommonUtils.set_int(self.p_limit.get(), 0), id=illu.id,
                                illu=illu, title="WebPageRanking_" + mode + "_" + date, get_from='Web Page Ranking')
                    tasks.append(task)
            else:
                print ('warning', 'pixiv web page  Ranking results are empty')
                showerror("error", 'pixiv web page Ranking results are empty')
        all_count = len(tasks)
        if all_count > 0:
            current_count = AtomicInteger.AtomicInteger()
            if not os.path.exists(path):
                os.makedirs(path)
            for task in tasks:
                task.all_count = all_count
                task.current_count = current_count
                self.queue.add_work(task)
