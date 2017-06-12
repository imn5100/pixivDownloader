# -*- coding: utf-8 -*-
import re

from utils.Config import Config


def testConfig():
    config = Config('../config.ini', "pixiv")
    print config.get("SEARCH_KEYWORD", "kaka")

def testMatch():
    url = "https://www.pixivision.net/zh/c/illustration/"
    print re.match(r"htt(p|ps)://www.pixivision.net/(zh|ja|en|zh-tw)/c/illustration(/|)(\?p=\d+|)", url)


if __name__ == '__main__':
    testMatch()
