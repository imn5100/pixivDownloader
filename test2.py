# -*- coding: utf-8 -*-
from utils.Config import Config


def testConfig():
    config = Config('../config.ini', "pixiv")
    print config.get("SEARCH_KEYWORD", "kaka")


if __name__ == '__main__':
    testConfig()
