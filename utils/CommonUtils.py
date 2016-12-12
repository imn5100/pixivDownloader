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
        topic_file = codecs.open(file_path, 'a', encoding='utf-8')
        topic_file.write("description = " + data["description"] + "\n")
        topic_file.write("IlluNum = " + str(data["size"]) + "\n")
        if flag == 1:
            topic_file.write("title = " + data["title"] + "\n")
    except Exception, e:
        print("Write Topic Description Fail")
        print(e)
    finally:
        topic_file.close()


def check_image(dir):
    if os.path.exists(dir):
        # windows系统获取的文件夹名称为GBK编码
        image_fls = os.listdir(dir)
        for image_fl in image_fls:
            # 文件夹名称 widnows获取为gbk，liunx如果默认编码为utf-8则不需要这一步
            image_fl = image_fl.decode("gbk")
            # 检查是否有特辑描述文件
            base_path = dir + "/" + image_fl
            if os.path.exists(base_path + "/topic.txt"):
                check_num(base_path)
            else:
                print("Not found topic.txt.\tPath：" + dir + "/" + image_fl.encode("utf-8"))


def check_num(base_path):
    import re
    true_image_num = len(os.listdir(base_path))
    content = open(base_path + "/topic.txt", "r").read()
    res = re.search("IlluNum = \d*", content)
    if res:
        image_num = re.search("IlluNum = \d*", content).group().split(" ")[-1]
        if int(true_image_num) - int(image_num) == 1:
            print("All illustrations have been downloaded.\tPath:" + base_path)
        else:
            print(base_path + " " + str(int(true_image_num) - 1) + "/" + image_num)
    else:
        print("Not found IlluNum.\tPath:" + base_path + "/topic.txt")


if __name__ == '__main__':
    check_image("E:/imageDownLoad/pixivision")
