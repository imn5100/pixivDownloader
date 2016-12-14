# -*- coding: utf-8 -*-

class RedisFilter(object):
    def __init__(self, server, block_num=3, filter_key='default_filter'):
        self.block_num = block_num
        self.filter_key = filter_key
        self.server = server

    def add(self, data):
        self.server.sadd(self.get_key(data), data)

    def remove(self, data):
        self.server.srem(self.get_key(data), data)

    def add_all(self, datas):
        p = self.server.pipeline()
        for data in datas:
            p.sadd(self.get_key(data), data)
        p.execute()

    def remove_all(self, datas):
        p = self.server.pipeline()
        for data in datas:
            p.srem(self.get_key(data), data)
        p.execute()

    def is_contained(self, data):
        return self.server.sismember(self.get_key(data), data)

    def block_index(self, value):
        return hash(value) % self.block_num + 1

    def get_key(self, value):
        return self.filter_key + str(self.block_index(value))
