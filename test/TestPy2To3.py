import datetime
# Tkinter to  tkinter
from tkinter import *
from tkinter import ttk, messagebox, scrolledtext

import requests
# BeautifulSoup to bs4
# pip3 install beautifulsoup4
from bs4 import BeautifulSoup
# Queue to queue
from queue import Queue
# Configparser to  configparser
import configparser
import urllib.parse as urlparse

import time

ranking_mode = ('day', 'week', 'month', 'day_male', 'day_female', 'week_original', 'week_rookie',
                'day_r18', 'week_r18'
                )
BASE_URL = "http://www.pixivision.net"


class DictObj(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


# 将dict 转换为对象
def parse_dict(data_dict):
    o = DictObj()
    for k, v in data_dict.items():
        o[str(k)] = v
    return o


class MainFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.page_number = StringVar(value=2)
        self.p_limit = StringVar(value=10)
        self.path_var = StringVar(value='')
        self.mode_var = StringVar(value='day')
        #  %H:%M:%S
        self.date_var = StringVar(
            value=time.strftime("%Y-%m-%d", (datetime.datetime.now() - datetime.timedelta(days=1)).timetuple()))
        self.init()
        self.pack()

    def init(self):
        # ranking 组件
        mode_label = Label(self, text="Mode:", width=57, height=1)
        mode_label.pack()

        mode_box = ttk.Combobox(self, width=20, textvariable=self.mode_var, state='readonly')
        mode_box['values'] = ranking_mode
        mode_box.pack()
        mode_box.focus_displayof()

        date_label = Label(self, text="Ranking Date:", width=10, height=1)
        date_label.pack()

        date_entry = Entry(self, width=20, textvariable=self.date_var)
        date_entry.pack()

        page_label = Label(self, text="Number of pages:", width=30, height=1)
        page_label.pack()

        page_entry = Entry(self, width=57, textvariable=self.page_number)
        page_entry.pack()

        p_limit_label = Label(self, text="Single works P limit(0 does not limit):", width=30, height=1)
        p_limit_label.pack()

        p_limit_entry = Entry(self, width=57, textvariable=self.p_limit)
        p_limit_entry.pack()

        ranking_path_label = Label(self, text="Download Path:", width=30, height=1)
        ranking_path_label.pack()

        ranking_path_entry = Entry(self, width=57, textvariable=self.path_var)
        ranking_path_entry.pack()

        ranking_button = Button(self, text='Start', height=2, command=self.handle_ranking)
        ranking_button.pack()

    def handle_ranking(self):
        messagebox.showerror("111")


def parse_illustration_topic(html):
    if not html:
        return None
    main = BeautifulSoup(html, features="html.parser")
    lis = main.findAll("li", attrs={"class": "article-card-container"})
    datas = []
    for li in lis:
        try:
            data = {"label": li.find("span",
                                     attrs={"class": "arc__thumbnail-label _category-label large spotlight"}).text}
            a = li.find("h2", attrs={"class": "arc__title "}).find("a")
            data["href"] = BASE_URL + a["href"]
            data["title"] = a.text
            data["pub_time"] = li.find("time").text
            data["tags"] = []
            tags = li.findAll("div", attrs={"class": "tls__list-item small"})
            for tag in tags:
                data["tags"].append(tag.text)
            data = parse_dict(data)
            datas.append(data)
        except Exception as e:
            print("Get Topics Warning")
            print(e)
            continue
    return datas


def test_pixivision():
    topic_list = parse_illustration_topic(
        requests.get("http://www.pixivision.net/en/c/illustration/?p=1").text)
    for topic in topic_list:
        print(topic)


if __name__ == '__main__':
    # app = MainFrame()
    # app.master.title('hello world')
    # app.mainloop()
    test_pixivision()
