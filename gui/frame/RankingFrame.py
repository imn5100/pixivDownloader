# -*- coding: utf-8 -*-
import datetime
import os
import time
from Tkinter import *
from threading import Thread
from tkMessageBox import showwarning, showerror, showinfo

from tkinter import ttk

from gui.DownloadTask import Task, TASK_TYPE_RANKING, DOWNLOAD_MODE_DETAIL
from gui.frame.PixivFrame import PixivFrame
from pixiv_config import IMAGE_SAVE_BASEPATH
from utils import CommonUtils, AtomicInteger

ranking_mode = ('day', 'week', 'month', 'day_male', 'day_female', 'week_original', 'week_rookie',
                'day_r18', 'week_r18'
                )


class RankingFrame(PixivFrame):
    def __init__(self, master, name, queue, api):
        PixivFrame.__init__(self, master, name)
        self.queue = queue
        self.api = api
        self.page_number = StringVar(value=2)
        self.p_limit = StringVar(value=10)
        self.path_var = StringVar(value=IMAGE_SAVE_BASEPATH)
        self.mode_var = StringVar(value='day')
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
        mode_box['values'] = ranking_mode
        mode_box.pack()
        mode_box.focus_displayof()

        date_label = Label(self, text="Ranking Date:", width=10, height=1)
        date_label.pack()

        date_entry = Entry(self, width=20, textvariable=self.date_var)
        date_entry.pack()

        page_label = Label(self, text="Number of pages:", width=30, height=1)
        page_label.pack()

        page_entry = Entry(self, width=57, textvariable=self.page_number)
        page_entry.pack()

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
        page = CommonUtils.set_int(self.page_number.get(), 2)
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
        ranking_handler = Thread(target=self.ranking, args=(path, mode, date, page))
        ranking_handler.start()

    def ranking(self, path, mode, date, pages=1):
        path = path + "/ranking_" + mode + '_' + date
        page = 0
        offset = 0
        tasks = []
        while page < pages:
            ranking_data = self.api.app_ranking(mode=mode, date=date, offset=offset).illusts
            page = page + 1
            if len(ranking_data) > 0:
                print ('Get from ranking(page=' + str(page) + '):' + str(len(ranking_data)))
                for illu in ranking_data:
                    task = Task(TASK_TYPE_RANKING, DOWNLOAD_MODE_DETAIL, path=path,
                                p_limit=CommonUtils.set_int(self.p_limit.get(), 0),
                                illu=illu, title="ranking_" + mode + "_" + date, get_from='ranking')
                    tasks.append(task)
                    offset = offset + 1
            else:
                print ('warning', 'Ranking(page=' + str(page) + ') results are empty')
                showerror("error", 'Ranking(page=' + str(page) + ') results are empty')
                break
        all_count = len(tasks)
        if all_count > 0:
            current_count = AtomicInteger.AtomicInteger()
            if not os.path.exists(path):
                os.makedirs(path)
            for task in tasks:
                task.all_count = all_count
                task.current_count = current_count
                self.queue.add_work(task)
