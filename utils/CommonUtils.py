# -*- coding: utf-8 -*-
import codecs
import os
import urlparse

import re


def get_url_param(url, param):
    try:
        result = urlparse.urlparse(url)
        return urlparse.parse_qs(result.query)[param][0]
    except:
        return None


def filter_dir_name(name):
    return re.sub('[\/:*?"<>.|]', '', name).strip()


def write_topic(file_path, topic):
    topci_file = codecs.open(file_path, 'w', encoding='utf-8')
    os.path.abspath(file_path)
    topci_file.write("Label = " + topic.label + "\n")
    topci_file.write("Title = " + topic.title + "\n")
    topci_file.write("Href = " + topic.href + "\n")
    topci_file.write("PubTime = " + topic.pub_time + "\n")
    tagstr = ""
    for tag in topic.tags:
        tagstr += " " + tag
    topci_file.write("Tag =" + tagstr + "\n")
    topci_file.close()
