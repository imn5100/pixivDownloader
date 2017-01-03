# -*- coding: utf-8 -*-
import json

import redis

from utils.LoggerUtil import error_log


class RedisMessageClient(object):
    def __init__(self, msg_handler=None, host="localhost", port=6379):
        self.msg_handler = msg_handler
        self.redis_client = redis.StrictRedis(host, port)
        self.ps = None

    # 必须发布已订阅的频道
    def pub(self, channel, message):
        return self.redis_client.publish(channel, message) == 1

    # 先启动订阅带能完成推送消息
    def run_sub(self, channel):
        self.ps = self.redis_client.pubsub()
        self.ps.subscribe(channel)
        for data in self.ps.listen():
            print(data)
            if data and data.has_key("type") and data["type"] == "message":
                self.msg_handler.handler_data(data["data"])


class PixivDownloadHandler(object):
    def __init__(self, pixiv_api):
        self.pixiv_api = pixiv_api

    def handler_data(self, illu):
        print(illu)
        illu = json.loads(illu)
        if illu.has_key("url"):
            if illu.has_key("path"):
                print("Download start" + illu["path"])
                self.pixiv_api.download(illu["url"], illu["path"])
            else:
                print("Download start" + illu["url"])
                self.pixiv_api.download(illu["url"])
        else:
            error_log("Error data:" + str(illu))
