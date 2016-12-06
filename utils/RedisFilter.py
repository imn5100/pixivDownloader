# -*- coding: utf-8 -*-
from pixiv_config import BLOCK_NUM, REDIS_FILTER_KEY


class RedisFilter(object):
    def __init__(self, server):
        self.server = server

    def add(self, data):
        self.server.sadd(RedisFilter.get_key(data), data)

    def remove(self, data):
        self.server.srem(RedisFilter.get_key(data), data)

    def add_all(self, datas):
        p = self.server.pipeline()
        for data in datas:
            p.sadd(RedisFilter.get_key(data), data)
        p.execute()

    def remove_all(self, datas):
        p = self.server.pipeline()
        for data in datas:
            p.srem(RedisFilter.get_key(data), data)
        p.execute()

    def is_contained(self, data):
        return self.server.sismember(RedisFilter.get_key(data), data)

    @classmethod
    def block_index(cls, value, block_num=3):
        if BLOCK_NUM:
            block_num = BLOCK_NUM
        return hash(value) % block_num + 1

    @classmethod
    def get_key(cls, value):
        return REDIS_FILTER_KEY + str(RedisFilter.block_index(value))
