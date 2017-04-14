# -*- coding: utf-8 -*-
import os
from Tkinter import *
from tkMessageBox import showerror, showwarning, showinfo


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

        url_label = Label(self, text="Pixiv(Pixivision) Site Or Illustration Id:", width=30, height=1)
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
        path = self.url_var.get().strip()
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception, e:
                showerror("error", e.message)
        if url == '' or path == '':
            showwarning("warning", "url or path can't be empty!")
            return
        if re.match("http://www.pixivision.net/(zh|ja|en|zh-tw)/a/\d*", url):
            showinfo("Info", "Start download pixivision.net page")
            return
        elif set_int(url) != 0:
            showinfo("Info", "Start download id:" + str(set_int(url)) + " illustration")
            return
        elif url.startswith("http"):
            showinfo("Info", "Start download this url")
        else:
            showerror("error", "invalid input")


if __name__ == '__main__':
    root = Tk()
    PixivDownloadFrame(root)
    root.mainloop()
