# -*- coding: utf-8 -*-
import os
from Tkinter import *
from tkMessageBox import showerror, showwarning, showinfo

from pixivision.ImageDownload import ImageDownload, IlluDownloadThread
from pixivision.PixivisionLauncher import PixivisionLauncher


def set_int(int_num):
    try:
        return int(int_num)
    except:
        return 0


class PixivDownloadFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.FrameSizeY = 250
        self.FrameSizeX = 465
        self.url_var = StringVar()
        self.path_var = StringVar()
        self.init_ui()

    def init_ui(self):
        self.root.title("Pixiv Downloader")
        screen_size_x = self.root.winfo_screenwidth()
        screen_size_y = self.root.winfo_screenheight()
        frame_pos_x = (screen_size_x - self.FrameSizeX) / 2
        frame_pos_y = (screen_size_y - self.FrameSizeY) / 2
        self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX, self.FrameSizeY, frame_pos_x, frame_pos_y))
        self.root.resizable(width=True, height=False)

        url_label = Label(self, text="Pixiv Or Pixivision Site Or Illustration Id:", width=50, height=1)
        url_label.pack()

        url_entry = Entry(self, width=50, textvariable=self.url_var)
        url_entry.pack()

        path_label = Label(self, text="Download Path:", width=30, height=1)
        path_label.pack()

        path_entry = Entry(self, width=50, textvariable=self.path_var)
        path_entry.pack()

        button = Button(self, text='Download', height=2, command=self.handle_url)
        button.pack()

        banner = Label(self, text="Power by imn5100", width=30, height=5)
        banner.pack()
        self.grid(row=0, column=0)

    def handle_url(self):
        url = self.url_var.get().strip()
        path = self.path_var.get().strip()
        if not os.path.exists(path):
            showerror("error", " No such file or directory!")
            return
        if url == '' or path == '':
            showwarning("warning", "url or path can't be empty!")
            return
        # 插画详情页下载
        if re.match("htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/a/\d*", url):
            showinfo("Info", "Start download pixivision.net page:" + url)
            IlluDownloadThread(url.strip(), path=path).start()
            return
        # 插画列表页下载
        elif re.match(r"htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/c/illustration/\?p=\d*", url):
            showinfo("Info", "Start download pixivision.net page:" + url)
            PixivisionLauncher(url, save_path=path).start()
            return
        elif set_int(url) != 0:
            showinfo("Info", "Downloading id:" + str(set_int(url)) + " illustration")
            ImageDownload.download_image_byid(url, path)
            return
        elif url.startswith("http"):
            # 无法解析的pixivison站 或非 pixiv站 不支持
            if url.find("pixivision.net") != -1:
                showerror("error", "The download link is not supported")
                return
            showinfo("Info", "Downloading  url:" + url)
            ImageDownload.download_byurl(url, path)
        else:
            showerror("error", "")


if __name__ == '__main__':
    root = Tk()
    PixivDownloadFrame(root)
    root.mainloop()
