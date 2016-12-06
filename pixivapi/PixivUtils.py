# -*- coding:utf-8 -*-
import json


class PixivError(Exception):
    def __init__(self, reason, header=None, body=None):
        self.reason = str(reason)
        self.header = header
        self.body = body
        super(Exception, self).__init__(self, reason)

    def __str__(self):
        return self.reason


class DictObj(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


# 将response转换为对象
def parse_resp(resp):
    try:
        return parse_json(resp.content)
    except Exception as e:
        raise PixivError("parse_json() error: %s" % e, header=resp.headers, body=resp.text)


# 将dict 转换为对象
def parse_dict(data_dict):
    o = DictObj()
    for k, v in data_dict.items():
        o[str(k)] = v
    return o


# 将json串转换为对象
def parse_json(json_str):
    return json.loads(json_str, object_hook=parse_dict)
