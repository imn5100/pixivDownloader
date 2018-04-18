# -*- coding: utf-8 -*-
from ScrolledText import ScrolledText
from Tkinter import *

from gui.WorkQueue import PixivQueue
from gui.frame.DownloadFrame import DownloadFrame
from gui.frame.RankingFrame import RankingFrame
from gui.frame.SearchFrame import SearchFrame
from pixiv.IllustrationDownloader import IllustrationDownloader
from pixivapi.PixivUtils import PixivError


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
        self.frames = [DownloadFrame(self, 'By Url or Id', self.queue, self.api, self.task_text),
                       SearchFrame(self, 'By Search', self.queue, self.api, self.search_handler),
                       RankingFrame(self, 'By Ranking', self.queue, self.api)]
        self.switch_menu = None
        self.init_ui()

    def init_ui(self):
        self.root.title("Pixiv Downloader")
        self.root.resizable(width=False, height=False)
        menubar = Menu(self)
        self.root.config(menu=menubar)
        self.switch_menu = Menu(menubar, tearoff=0)
        for frame in self.frames:
            frame.init_ui()
            frame.set_frames(self.frames)
            self.switch_menu.add_command(label=frame.name, command=frame.switch)
        menubar.add_cascade(label="Download Mode Switch", menu=self.switch_menu)
        # 公共组件
        text1 = ScrolledText(self, height=20, width=30, bg='light gray')
        # text1.bind("<Key>", lambda e: "break")
        text1.insert(END, 'Download Completed:\n')
        self.task_text = text1
        text2 = ScrolledText(self, height=20, width=40, bg='light gray')
        text2.tag_configure('info', foreground='#3A98FE')
        text2.tag_configure('warning', foreground='#ff9900')
        text2.tag_configure('error', foreground='#FF2D21')
        quote = "Console Log:\n"
        text2.insert(END, quote, 'info')
        self.print_text = text2
        text1.grid(row=3, column=0, sticky=W)
        text2.grid(row=3, column=1, sticky=W)

        banner = Label(self, text="Power by imn5100", width=30, height=5)
        banner.grid(row=4, columnspan=2)

        self.grid()
        self.frames[0].grid(row=1, columnspan=2)
        self.queue.run()

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
