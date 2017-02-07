# -*- coding: utf-8 -*-
import os


def get_url_param(url, param):
    import urlparse
    try:
        result = urlparse.urlparse(url)
        return urlparse.parse_qs(result.query)[param][0]
    except:
        return None


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
