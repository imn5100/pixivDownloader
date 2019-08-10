# -*- coding: utf-8 -*-
from Tkinter import *
from tkMessageBox import showerror

from gui.DownloaderFrame import PixivDownloadFrame
from pixiv import PixivDataDownloader
from pixiv_config import USERNAME, PASSWORD, PIXIV_COOKIES
from pixivapi.AuthPixivApi import AuthPixivApi
from utils.CommonUtils import is_empty


class LoginFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.api = None
        self.pixiv_data_handler = None
        self.root = root
        self.account = StringVar(value=USERNAME)
        self.password = StringVar(value=PASSWORD)
        self.init_ui()

    def init_ui(self):
        self.root.title("Pixiv Downloader")
        self.root.resizable(width=False, height=False)
        if not self.check_config():
            account_label = Label(self, text="Pixiv Account:", width=30,
                                  height=1)
            account_label.pack()
            account_entry = Entry(self, width=57, textvariable=self.account)
            account_entry.pack()
            pwd_label = Label(self, text="Password", width=30, height=1)
            pwd_label.pack()
            pwd_entry = Entry(self, width=57, textvariable=self.password)
            pwd_entry.pack()
            pwd_entry['show'] = '*'

            login_button = Button(self, text='Start', height=2, command=self.handler_login)
            login_button.pack()

            banner = Label(self, text="Power by imn5100", width=30, height=5)
            banner.pack()
            self.grid()

    def handler_login(self):
        username = self.account.get().strip()
        password = self.password.get().strip()
        if is_empty(username) or is_empty(password):
            showerror("error",
                      "Please input username and password")
            return
        try:
            if not self.api:
                self.api = AuthPixivApi(username, password)
                if not self.api.check_login_success():
                    showerror("error",
                              "[ERROR] auth() failed! Please check username and password")
                    return
            if not self.pixiv_data_handler:
                self.pixiv_data_handler = PixivDataDownloader.PixivDataHandler(username=username, password=password)
                if not self.pixiv_data_handler.check_login_success():
                    showerror("error",
                              "[ERROR] auth() failed! Please check username and password")
                    return
            frame = PixivDownloadFrame(self.root, self.api, self.pixiv_data_handler)
            sys.stdout = LogRedirection(frame.print_text)
            self.destroy()
        except Exception as e:
            print (e)
            showerror("error",
                      "[ERROR] auth() failed! Please check username and password")

    def check_config(self):
        success = False
        self.api = AuthPixivApi.get_authApi_by_token()
        if self.api:
            success = True
        if len(PIXIV_COOKIES) > 3:
            try:
                self.pixiv_data_handler = PixivDataDownloader.PixivDataHandler(cookies=PIXIV_COOKIES)
            except Exception as e:
                print (e)
            if self.pixiv_data_handler and self.pixiv_data_handler.check_login_success():
                print ("Cookie is correct!")
                if success:
                    frame = PixivDownloadFrame(self.root, self.api, self.pixiv_data_handler)
                    sys.stdout = LogRedirection(frame.print_text)
                    self.destroy()
                    return True
            else:
                self.pixiv_data_handler = None
                print ("Cookie error or expired!")

        return False


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
