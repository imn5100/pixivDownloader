# -*- coding: utf-8 -*-
import os
from Tkinter import *
from tkMessageBox import showerror, showwarning, showinfo

from pixiv_config import IMAGE_SVAE_BASEPATH
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
        self.print_text = None
        self.root = root
        self.FrameSizeY = 250
        self.FrameSizeX = 465
        self.url_var = StringVar()
        self.path_var = StringVar()
        self.path_var.set(IMAGE_SVAE_BASEPATH)
        self.init_ui()

    def init_ui(self):
        self.root.title("Pixiv Downloader")
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

        text2 = Text(self, height=20, width=50)
        scroll = Scrollbar(self, command=text2.yview)
        # 设置输出控制台只读，不接受按键事件,但会导致无法复制控制台的信息，暂时不限制
        # text2.bind("<Key>", lambda e: "break")
        text2.configure(yscrollcommand=scroll.set)
        text2.tag_configure('info', foreground='#3A98FE',
                            font=('Tempus Sans ITC', 12))
        text2.tag_configure('warning', foreground='#FEC534',
                            font=('Tempus Sans ITC', 12))
        text2.tag_configure('error', foreground='#FF2D21',
                            font=('Tempus Sans ITC', 12))
        quote = "This is Console:\n"
        text2.insert(END, quote, 'info')
        text2.pack()
        self.print_text = text2
        scroll.pack(side=RIGHT, fill=Y)
        self.grid(row=0, column=0)

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
            IlluDownloadThread(url.strip(), path=path, quality=1, create_path=True).start()
            return
        # 插画列表页下载
        elif re.match(r"htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/c/illustration/\?p=\d*", url):
            showinfo("info", "Start download pixivision.net page:" + url)
            print ("info", "Start download pixivision.net page:" + url)
            PixivisionLauncher(url, save_path=path).start()
            return
        elif set_int(url) != 0:
            showinfo("info", "Downloading id:" + str(set_int(url)) + " illustration")
            print ("info", "Downloading id:" + str(set_int(url)) + " illustration")
            ImageDownload.download_image_byid(url, path)
            return
        elif url.startswith("http"):
            # 无法解析的pixivison站 或非 pixiv站 不支持
            if url.find("pixivision.net") != -1:
                showerror("error", "The download link is not supported")
                print ("error", "The download link is not supported")
                return
            showinfo("info", "Downloading  url:" + url)
            print ("info", "Downloading  url:" + url)
            ImageDownload.download_byurl(url, path)
        else:
            showerror("error", "")


class LogRedirection:
    def __init__(self, text):
        self.text = text
        self.__console__ = sys.stdout

    def write(self, output_stream):
        try:
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


if __name__ == '__main__':
    root = Tk()
    frame = PixivDownloadFrame(root)
    sys.stdout = LogRedirection(frame.print_text)
    root.mainloop()
