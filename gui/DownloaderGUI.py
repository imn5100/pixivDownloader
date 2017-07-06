# -*- coding: utf-8 -*-
import os
from Tkinter import *
from threading import Thread
from tkMessageBox import showerror, showwarning, showinfo

from gui.WorkQueue import PixivQueue
from pixiv import PixivDataDownloader
from pixiv_config import IMAGE_SAVE_BASEPATH, USERNAME, PASSWORD, PIXIV_COOKIES
from pixivision.ImageDownload import IlluDownloadThread
from pixivision.PixivisionLauncher import PixivisionLauncher
from utils import CommonUtils


class PixivDownloadFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.queue = PixivQueue(callback=self.download_callback)
        self.print_text = None
        self.task_text = None
        self.root = root
        self.search_frame = Frame(self)
        self.download_frame = Frame(self)
        self.url_var = StringVar()
        self.keywords = StringVar(value='1000users入り')
        self.page_number = StringVar(value=2)
        self.fav_num = StringVar(value=500)
        self.p_limit = StringVar(value=20)
        self.path_var = StringVar(value=IMAGE_SAVE_BASEPATH)
        self.account = StringVar(value=USERNAME)
        self.password = StringVar(value=PASSWORD)
        self.search_status = False
        self.switch_menu = None
        self.init_ui()

    def init_ui(self):
        self.root.title("Pixiv Downloader")
        self.root.resizable(width=False, height=False)
        menubar = Menu(self)
        self.root.config(menu=menubar)
        self.switch_menu = Menu(menubar, tearoff=0)
        self.switch_menu.add_command(label="ToSearchDownload", command=self.switch)
        menubar.add_cascade(label="Download Mode Switch", menu=self.switch_menu)
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

        account_label = Label(self.search_frame, text="Pixiv Account(Use cookies ignore this):", width=30,
                              height=1)
        account_label.pack()
        account_entry = Entry(self.search_frame, width=57, textvariable=self.account)
        account_entry.pack()
        pwd_label = Label(self.search_frame, text="Password", width=30, height=1)
        pwd_label.pack()
        pwd_entry = Entry(self.search_frame, width=57, textvariable=self.password)
        pwd_entry.pack()
        pwd_entry['show'] = '*'

        search_button = Button(self.search_frame, text='Start', height=2, command=self.handle_search)
        search_button.pack()

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
        text2.tag_configure('warning', foreground='#FEC534')
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
            IlluDownloadThread(url.strip(), path=path, quality=1, create_path=True).register_hook(
                success_callback=self.download_callback).start()
            return
        # 插画列表页下载
        elif re.match(r"htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/c/illustration(/|)(\?p=\d+|)", url):
            showinfo("info", "Start download pixivision.net page:" + url)
            print ("info", "Start download pixivision.net page:" + url)
            PixivisionLauncher(url, save_path=path).register_hook(
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
        if len(PIXIV_COOKIES) >= 3:
            data_handler = PixivDataDownloader.PixivDataHandler(cookies=PIXIV_COOKIES)
        else:
            if CommonUtils.is_not_empty(self.account.get()) and CommonUtils.is_not_empty(self.password.get()):
                data_handler = PixivDataDownloader.PixivDataHandler(self.account.get().strip(),
                                                                    self.password.get().strip())
            else:
                showwarning("warning", "Please configure cookies or account and password!")
                print ("warning", "Please configure cookies or account and password!")
                return
        keywords = self.keywords.get()
        if CommonUtils.is_empty(keywords):
            showwarning("warning", "Please enter search keywords!")
            print ("warning", "Please enter search keywords!")
            return
        if CommonUtils.is_empty(self.path_var.get()):
            showwarning("warning", "path can't be empty!")
            print ("warning", "path can't be empty!")
            return
        path = self.path_var.get()
        if not os.path.exists(path):
            showerror("error", " No such file or directory!")
            print ('error', 'No such file or directory')
            return
        path = path + "/" + CommonUtils.filter_dir_name("search_" + keywords)
        if not os.path.exists(path):
            os.makedirs(path)
        showinfo("info", "Is searching：")
        search_handler = Thread(target=self.search, args=(data_handler, keywords, path))
        search_handler.start()

    def search(self, data_handler, keywords, path):
        set_filter = set()
        for p in range(1, CommonUtils.set_int(self.page_number.get(), 2) + 1):
            result = data_handler.search(keywords, page=p,
                                         download_threshold=CommonUtils.set_int(self.fav_num.get(), 0))
            for illu in result:
                if illu.url in set_filter:
                    continue
                else:
                    illu['search_path'] = path
                    illu['p_limit'] = CommonUtils.set_int(self.p_limit.get(), 0)
                    self.queue.add_work(illu)
                    set_filter.add(illu.url)

    def switch(self):
        if self.search_status:
            self.search_frame.grid_forget()
            self.download_frame.grid(row=1, columnspan=2)
            self.search_status = False
            self.switch_menu.entryconfig(0, label="ToSearchDownload")
        else:
            self.search_frame.grid(row=1, columnspan=2)
            self.download_frame.grid_forget()
            self.search_status = True
            self.switch_menu.entryconfig(0, label="ToUrlDownload")

    def download_callback(self, msg=None):
        if msg:
            self.task_text.insert(END, msg)
        else:
            self.task_text.insert(END, "A work Done")


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
            self.text.insert(END, output_stream, 'info')
        except Exception:
            self.text.insert(END, output_stream, 'info')

    def reset(self):
        sys.stdout = self.__console__

    def set_out(self):
        sys.stdout = self
