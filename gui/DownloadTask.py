# -*- coding: utf-8 -*-
from pixivapi.PixivUtils import DictObj

TASK_TYPE_ID = 1
TASK_TYPE_URL = 2
TASK_TYPE_SEARCH = 3
TASK_TYPE_SEARCH_API = 4
TASK_TYPE_RANKING = 5


class Task(DictObj):
    def __init__(self, task_type, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.task_type = task_type


if __name__ == '__main__':
    task = Task(TASK_TYPE_ID, **{"id": 1, 'path': "/", "url": "https://pixiv.net"})
    print (task.task_type)
    print (task.path)
    print (task.id)
    print (task.url)
