# -*- coding: utf-8 -*-
from Tkinter import *
from tkMessageBox import showerror

from gui.DownloaderFrame import PixivDownloadFrame, LogRedirection
from pixiv import PixivDataDownloader
from pixiv_config import USERNAME, PASSWORD, ACCESS_TOKEN, PIXIV_COOKIES
from pixivapi.AuthPixivApi import AuthPixivApi
from utils.CommonUtils import is_not_empty


class LoginFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.account = StringVar(value=USERNAME)
        self.password = StringVar(value=PASSWORD)
        # self.token = StringVar(value='')
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

            # token_label = Label(self, text="You can ignore the above only input token:", width=30, height=1)
            # token_label.pack()
            # token_entry = Entry(self, width=57, textvariable=self.token)
            # token_entry.pack()

            login_button = Button(self, text='Start', height=2, command=self.handler_login)
            login_button.pack()

            banner = Label(self, text="Power by imn5100", width=30, height=5)
            banner.pack()
            self.grid()

    def handler_login(self):
        username = self.account.get().strip()
        password = self.password.get().strip()
        # token = self.token.get().strip()
        use_token = True
        try:
            # if token:
            #     api = AuthPixivApi('', '', token)
            if is_not_empty(username) and is_not_empty(password):
                use_token = False
                api = AuthPixivApi(username, password)
            else:
                showerror("error",
                          "Please input username and password")
                return
            if api.check_login_success():
                frame = PixivDownloadFrame(self.root, api)
                sys.stdout = LogRedirection(frame.print_text)
                self.destroy()
            else:
                showerror("error",
                          "[ERROR] auth() failed! Please check " + ("token" if use_token else "username and password"))
        except Exception as e:
            print (e)
            showerror("error",
                      "[ERROR] auth() failed! Please check " + ("token" if use_token else "username and password"))

    def check_config(self):
        if ACCESS_TOKEN and len(PIXIV_COOKIES) > 3:
            api = AuthPixivApi('', '', ACCESS_TOKEN)
            if api.check_login_success():
                search_handler = PixivDataDownloader.PixivDataHandler(cookies=PIXIV_COOKIES)
                if search_handler.check_login_success():
                    frame = PixivDownloadFrame(self.root, api, search_handler=search_handler)
                    sys.stdout = LogRedirection(frame.print_text)
                    self.destroy()
                    return True
                else:
                    print "PIXIV_COOKIES config Wrong"
            else:
                print "ACCESS_TOKEN config Wrong!"
        return False
