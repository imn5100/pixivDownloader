# -*- coding: utf-8 -*-
from Tkinter import *
from tkMessageBox import showwarning, showerror, showinfo

import os

from gui.DownloadTask import TASK_TYPE_ID, Task, TASK_TYPE_URL
from gui.frame.PixivFrame import PixivFrame
from pixiv.IllustrationDownloader import IllustrationDownloader
from pixiv_config import IMAGE_SAVE_BASEPATH
from pixivision.PixivisionLauncher import PixivisionLauncher
from pixivision.PixivisionTopicDownloader import IlluDownloadThread
from utils import CommonUtils


class DownloadFrame(PixivFrame):
    def __init__(self, master, name, queue, api, task_text):
        PixivFrame.__init__(self, master, name)
        self.queue = queue
        self.downloader = IllustrationDownloader(api)
        self.api = api
        self.url_var = StringVar()
        self.task_text = task_text
        self.path_var = StringVar(value=IMAGE_SAVE_BASEPATH)

    def init_ui(self):
        self.init_url_id()

    def init_url_id(self):
        # 基本下载组件
        url_label = Label(self, text="Pixiv Or Pixivision Site Or Illustration Id:", width=57, height=1)
        url_label.pack()

        url_entry = Entry(self, width=57, textvariable=self.url_var)
        url_entry.pack()

        path_label = Label(self, text="Download Path:", width=30, height=1)
        path_label.pack()

        path_entry = Entry(self, width=57, textvariable=self.path_var)
        path_entry.pack()

        button = Button(self, text='Download', height=2, command=self.handle_url)
        button.pack()

    def handle_url(self):
        url = self.url_var.get().strip()
        path = self.path_var.get().strip()
        if url == '' or path == '':
            showwarning("warning", "url or path can't be empty!")
            print ("warning", "url or path can't be empty!")
            return
        if not os.path.exists(path):
            showerror("error", " No such file or directory!")
            print ('error', 'No such file or directory')
            return
        # 插画详情页下载
        if re.match("htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/a/\d*", url):
            showinfo("info", "Start download pixivision.net page:" + url)
            print ("info", "Start download pixivision.net page:" + url)
            IlluDownloadThread(url.strip(), path=path, create_path=True, downloader=self.downloader).register_hook(
                success_callback=self.download_callback).start()
            return
        # 插画列表页下载
        elif re.match(r"htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/c/illustration(/|)(\?p=\d+|)", url):
            showinfo("info", "Start download pixivision.net page:" + url)
            print ("info", "Start download pixivision.net page:" + url)
            PixivisionLauncher(url, save_path=path, downloader=self.downloader).register_hook(
                success_callback=self.download_callback).start()
            return
        elif CommonUtils.set_int(url) != 0:
            showinfo("info", "Downloading id:" + str(CommonUtils.set_int(url)) + " illustration")
            print ("info", "Downloading id:" + str(CommonUtils.set_int(url)) + " illustration")
            self.queue.add_work(Task(TASK_TYPE_ID, id=CommonUtils.set_int(url), path=path))
            return
        elif url.startswith("http"):
            # 无法解析的pixivison站 或非 pixiv站 不支持
            if url.find("pixivision.net") != -1:
                showerror("error", "The download link is not supported")
                print ("error", "The download link is not supported")
                return
            showinfo("info", "Downloading  url:" + url)
            print ("info", "Downloading  url:" + url)
            self.queue.add_work(Task(TASK_TYPE_URL, url=url, path=path))
        else:
            showerror("error", "")

    def download_callback(self, msg=None):
        """
        任务完成回调
        :param msg: 回调消息
        :return: none
        """
        if msg:
            self.task_text.insert(END, msg)
        else:
            self.task_text.insert(END, "A work Done\n")
