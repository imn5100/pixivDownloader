# -*- coding: utf-8 -*-
import os
from Tkinter import *
from threading import Thread
from tkMessageBox import showerror, showwarning, showinfo

import time

import datetime
from tkinter import ttk

from gui.WorkQueue import PixivQueue
from pixiv.IllustrationDownloader import IllustrationDownloader
from pixiv_config import IMAGE_SAVE_BASEPATH, DOWNLOAD_THRESHOLD
from pixivapi.PixivUtils import PixivError
from pixivision.PixivisionLauncher import PixivisionLauncher
from pixivision.PixivisionTopicDownloader import IlluDownloadThread
from utils import CommonUtils

ranking_mode = ('day', 'week', 'month', 'day_male', 'day_female', 'week_original', 'week_rookie',
                'day_r18', 'week_r18'
                )


# 'day_r18', 'week_r18'


class PixivDownloadFrame(Frame):
    def __init__(self, root, api, search_handler):
        Frame.__init__(self, root)
        if not search_handler or not api:
            raise PixivError('You must set  authPixivApi and search_handler for the DownloadFrame')
        self.api = api
        self.search_handler = search_handler
        self.downloader = IllustrationDownloader(api)
        self.queue = PixivQueue(self.downloader, callback=self.download_callback)
        self.print_text = None
        self.task_text = None
        self.root = root
        self.search_frame = Frame(self)
        self.download_frame = Frame(self)
        self.ranking_frame = Frame(self)
        self.url_var = StringVar()
        self.keywords = StringVar(value='1000users入り')
        self.page_number = StringVar(value=2)
        self.fav_num = StringVar(value=500)
        self.p_limit = StringVar(value=10)
        self.path_var = StringVar(value=IMAGE_SAVE_BASEPATH)
        self.mode_var = StringVar(value='day')
        #  %H:%M:%S
        self.date_var = StringVar(
            value=time.strftime("%Y-%m-%d", (datetime.datetime.now() - datetime.timedelta(days=1)).timetuple()))
        self.switch_menu = None
        self.init_ui()

    def init_ui(self):
        self.root.title("Pixiv Downloader")
        self.root.resizable(width=False, height=False)
        menubar = Menu(self)
        self.root.config(menu=menubar)
        self.switch_menu = Menu(menubar, tearoff=0)
        self.switch_menu.add_command(label="By Url or Id", command=self.switch_url)
        self.switch_menu.add_command(label="By Search", command=self.switch_search)
        self.switch_menu.add_command(label="By Ranking", command=self.switch_ranking)
        menubar.add_cascade(label="Download Mode Switch", menu=self.switch_menu)

        self.init_url_id()
        self.init_search()
        self.init_ranking()

        # 公共组件
        text1 = Text(self, height=20, width=30, bg='light gray')
        text1.bind("<Key>", lambda e: "break")
        text1.insert(END, 'Download Completed:\n')
        self.task_text = text1
        text2 = Text(self, height=20, width=40, bg='light gray')
        scroll = Scrollbar(self, command=text2.yview)
        scroll2 = Scrollbar(self, command=text1.yview)
        text1.configure(yscrollcommand=scroll2.set)
        text2.configure(yscrollcommand=scroll.set)
        text2.tag_configure('info', foreground='#3A98FE')
        text2.tag_configure('warning', foreground='#ff9900')
        text2.tag_configure('error', foreground='#FF2D21')
        quote = "Console Log:\n"
        text2.insert(END, quote, 'info')
        self.print_text = text2
        text1.grid(row=3, column=0, sticky=W)
        scroll2.grid(row=3, column=0, sticky=N + S + E)
        text2.grid(row=3, column=1, sticky=W)
        scroll.grid(row=3, column=1, sticky=N + S + E)

        banner = Label(self, text="Power by imn5100", width=30, height=5)
        banner.grid(row=4, columnspan=2)

        self.download_frame.grid(row=1, columnspan=2)
        self.grid()
        self.queue.run()

    def init_url_id(self):
        # 基本下载组件
        url_label = Label(self.download_frame, text="Pixiv Or Pixivision Site Or Illustration Id:", width=57, height=1)
        url_label.pack()

        url_entry = Entry(self.download_frame, width=57, textvariable=self.url_var)
        url_entry.pack()

        path_label = Label(self.download_frame, text="Download Path:", width=30, height=1)
        path_label.pack()

        path_entry = Entry(self.download_frame, width=57, textvariable=self.path_var)
        path_entry.pack()

        button = Button(self.download_frame, text='Download', height=2, command=self.handle_url)
        button.pack()

    def init_search(self):
        # search组件
        keywords_label = Label(self.search_frame, text="Key Words:", width=57, height=1)
        keywords_label.pack()

        keywords_entry = Entry(self.search_frame, width=57, textvariable=self.keywords)
        keywords_entry.pack()

        search_path_label = Label(self.search_frame, text="Download Path:", width=30, height=1)
        search_path_label.pack()

        search_path_entry = Entry(self.search_frame, width=57, textvariable=self.path_var)
        search_path_entry.pack()

        fav_num_label = Label(self.search_frame, text="Minimum number of favorites:", width=30, height=1)
        fav_num_label.pack()

        fav_num_entry = Entry(self.search_frame, width=57, textvariable=self.fav_num)
        fav_num_entry.pack()

        page_label = Label(self.search_frame, text="Number of pages:", width=30, height=1)
        page_label.pack()

        page_entry = Entry(self.search_frame, width=57, textvariable=self.page_number)
        page_entry.pack()

        p_limit_label = Label(self.search_frame, text="Single works P limit(0 does not limit):", width=30, height=1)
        p_limit_label.pack()

        p_limit_entry = Entry(self.search_frame, width=57, textvariable=self.p_limit)
        p_limit_entry.pack()

        search_button = Button(self.search_frame, text='Start', height=2, command=self.handle_search)
        search_button.pack()

    def init_ranking(self):
        # ranking 组件
        mode_label = Label(self.ranking_frame, text="Mode:", width=57, height=1)
        mode_label.pack()

        mode_box = ttk.Combobox(self.ranking_frame, width=20, textvariable=self.mode_var, state='readonly')
        mode_box['values'] = ranking_mode
        mode_box.pack()
        mode_box.focus_displayof()

        date_label = Label(self.ranking_frame, text="Ranking Date:", width=10, height=1)
        date_label.pack()

        date_entry = Entry(self.ranking_frame, width=20, textvariable=self.date_var)
        date_entry.pack()

        page_label = Label(self.ranking_frame, text="Number of pages:", width=30, height=1)
        page_label.pack()

        page_entry = Entry(self.ranking_frame, width=57, textvariable=self.page_number)
        page_entry.pack()

        p_limit_label = Label(self.ranking_frame, text="Single works P limit(0 does not limit):", width=30, height=1)
        p_limit_label.pack()

        p_limit_entry = Entry(self.ranking_frame, width=57, textvariable=self.p_limit)
        p_limit_entry.pack()

        ranking_path_label = Label(self.ranking_frame, text="Download Path:", width=30, height=1)
        ranking_path_label.pack()

        ranking_path_entry = Entry(self.ranking_frame, width=57, textvariable=self.path_var)
        ranking_path_entry.pack()

        ranking_button = Button(self.ranking_frame, text='Start', height=2, command=self.handle_ranking)
        ranking_button.pack()

    # 事件处理 #

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
            self.queue.add_work({
                'id': CommonUtils.set_int(url),
                'path': path + "/"
            })
            return
        elif url.startswith("http"):
            # 无法解析的pixivison站 或非 pixiv站 不支持
            if url.find("pixivision.net") != -1:
                showerror("error", "The download link is not supported")
                print ("error", "The download link is not supported")
                return
            showinfo("info", "Downloading  url:" + url)
            print ("info", "Downloading  url:" + url)
            self.queue.add_work({
                'url': url,
                'path': path + "/"
            })
        else:
            showerror("error", "")

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
        set_filter = set()
        page = CommonUtils.set_int(self.page_number.get(), 2)
        fav_num = CommonUtils.set_int(self.fav_num.get(), 0)
        for p in range(1, page + 1):
            result = self.search_handler.search(keywords, page=p,
                                                download_threshold=fav_num)
            if len(result) == 0:
                print ('warning', 'Page:' + str(p) + ' Search  results are Empty')
                continue
            if not os.path.exists(path):
                os.makedirs(path)
            for illu in result:
                if illu.url in set_filter:
                    continue
                else:
                    illu['search_path'] = path
                    illu['p_limit'] = CommonUtils.set_int(self.p_limit.get(), 0)
                    self.queue.add_work(illu)
                    set_filter.add(illu.url)
        api_search_data = api_search(keywords, self.api, page=page, download_threshold=fav_num)
        if len(api_search_data) == 0:
            print ('warning', 'Api search results are empty')
        else:
            if not os.path.exists(path):
                os.makedirs(path)
            for illu in api_search_data:
                illu['api_search_path'] = path
                illu['p_limit'] = CommonUtils.set_int(self.p_limit.get(), 0)
                self.queue.add_work(illu)

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
        path_exist = os.path.exists(path)
        while page < pages:
            ranking_data = self.api.app_ranking(mode=mode, date=date, offset=offset).illusts
            page = page + 1
            if len(ranking_data) > 0:
                if not path_exist:
                    os.makedirs(path)
                    path_exist = True
                print ('Get from ranking(page=' + str(page) + '):' + str(len(ranking_data)))
                for illu in ranking_data:
                    illu['ranking_path'] = path
                    illu['p_limit'] = CommonUtils.set_int(self.p_limit.get(), 0)
                    self.queue.add_work(illu)
                    offset = offset + 1
            else:
                print ('warning', 'Ranking(page=' + str(page) + ') results are empty')
                showerror("error", 'Ranking(page=' + str(page) + ') results are empty')
                break

    # 模式切换

    def switch_url(self):
        self.download_frame.grid(row=1, columnspan=2)
        self.search_frame.grid_forget()
        self.ranking_frame.grid_forget()

    def switch_search(self):
        self.search_frame.grid(row=1, columnspan=2)
        self.download_frame.grid_forget()
        self.ranking_frame.grid_forget()

    def switch_ranking(self):
        self.ranking_frame.grid(row=1, columnspan=2)
        self.search_frame.grid_forget()
        self.download_frame.grid_forget()

    def download_callback(self, msg=None):
        """
        任务完成回调
        :param msg: 回调消息
        :return: none
        """
        if msg:
            self.task_text.insert(END, msg)
        else:
            self.task_text.insert(END, "A work Done")


def api_search(keyword, api, page=1, download_threshold=DOWNLOAD_THRESHOLD):
    illusts = []
    if CommonUtils.is_empty(keyword):
        raise PixivError('[ERROR] keyword is empty')
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


class LogRedirection:
    def __init__(self, text):
        self.text = text
        self.__console__ = sys.stdout

    def write(self, output_stream):
        try:
            # 如果有必要可以在错误日志打印所有输出
            # LoggerUtil.error_log(output_stream)
            if output_stream.startswith('(') and output_stream.endswith(')'):
                output = eval(output_stream)
                if output and len(output) == 2:
                    self.text.insert(END, output[1], output[0])
                    return
            if output_stream.startswith('{"error":'):
                self.text.insert(END, output_stream, 'error')
                return
            self.text.insert(END, output_stream, 'info')
        except Exception:
            self.text.insert(END, output_stream, 'error')

    def reset(self):
        sys.stdout = self.__console__

    def set_out(self):
        sys.stdout = self
