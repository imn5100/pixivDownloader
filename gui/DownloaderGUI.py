# -*- coding: utf-8 -*-
import os
from Tkinter import *
from tkMessageBox import showerror, showwarning, showinfo

from gui.WorkQueue import PixivQueue
from pixiv_config import IMAGE_SVAE_BASEPATH
from pixivision.ImageDownload import IlluDownloadThread
from pixivision.PixivisionLauncher import PixivisionLauncher


def set_int(int_num):
    try:
        return int(int_num)
    except:
        return 0


class PixivDownloadFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.queue = PixivQueue(callback=self.download_callback)
        self.print_text = None
        self.task_text = None
        self.root = root
        self.FrameSizeY = 250
        self.FrameSizeX = 465
        self.url_var = StringVar()
        self.path_var = StringVar()
        self.path_var.set(IMAGE_SVAE_BASEPATH)
        self.init_ui()

    def init_ui(self):
        self.root.title("Pixiv Downloader")
        self.root.resizable(width=False, height=False)

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

        text1 = Text(self, height=20, width=30)
        text1.bind("<Key>", lambda e: "break")
        text1.insert(END, 'Download Completed:\n')
        text1.pack(side=LEFT)
        self.task_text = text1

        text2 = Text(self, height=20, width=40)
        scroll = Scrollbar(self, command=text2.yview)
        text2.configure(yscrollcommand=scroll.set)
        text2.tag_configure('info', foreground='#3A98FE')
        text2.tag_configure('warning', foreground='#FEC534')
        text2.tag_configure('error', foreground='#FF2D21')
        quote = "Console Log:\n"
        text2.insert(END, quote, 'info')
        text2.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)
        self.print_text = text2
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
                success_callback=self.thread_callback).start()
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
            self.queue.add_work({
                'id': set_int(url),
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

    def download_callback(self, illu_file, id=None, url=None):
        if id:
            msg = "{\nId:" + str(id)
        else:
            msg = "{\nUrl:" + str(url)
        self.task_text.insert(END, msg + "\nFile:" + illu_file + "\n}\n")

    def thread_callback(self):
        self.task_text.insert(END, "A work Done")


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
