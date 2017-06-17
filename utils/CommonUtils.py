# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


def get_url_param(url, param):
    import urlparse
    try:
        result = urlparse.urlparse(url)
        return urlparse.parse_qs(result.query)[param][0]
    except:
        return None


def set_int(int_num, default_value=0):
    try:
        return int(int_num)
    except:
        return default_value


def is_not_empty(val):
    if val is not None and val.strip() != '':
        return True
    return False


def is_empty(val):
    return not is_not_empty(val)


def filter_dir_name(name):
    import re
    return re.sub('[\/:*?"<>.|]', '', name).strip()


def write_topic(file_path, topic):
    import codecs
    topic_file = codecs.open(file_path, 'w', encoding='utf-8')
    topic_file.write("Label = " + topic.label + "\n")
    topic_file.write("Title = " + topic.title + "\n")
    topic_file.write("Href = " + topic.href + "\n")
    topic_file.write("PubTime = " + topic.pub_time + "\n")
    tagstr = ""
    for tag in topic.tags:
        tagstr += " " + tag
    topic_file.write("Tag =" + tagstr + "\n")
    topic_file.close()


def write_topic_des(file_path, data):
    import codecs
    try:
        flag = 0
        # topic.txt 不存在时 需要填写 title信息，否则不需要
        if not os.path.exists(file_path):
            flag = 1
        topic_file = codecs.open(file_path, 'a+', encoding='utf-8')
        # 已写入过 下载数量则跳过写入
        if topic_file.read().find("IlluNum") > 0:
            return
        topic_file.write("description = " + data["description"] + "\n")
        topic_file.write("IlluNum = " + str(data["size"]) + "\n")
        if flag == 1:
            topic_file.write("title = " + data["title"] + "\n")
    except Exception, e:
        print("Write Topic Description Fail")
        print(e)


# 构建回掉通知消息
def build_callback_msg(path, id=None, url=None, keywords=None):
    if id:
        show = "Id"
        show1 = id
    elif url:
        show = "Url"
        show1 = url
    elif keywords:
        show = 'Keywords'
        show1 = keywords
    if path:
        show2 = path
    else:
        show2 = "Download Fail"
    msg = "{\n%s:%s\nFile:%s\n}\n"
    return msg % (show, show1, show2)
