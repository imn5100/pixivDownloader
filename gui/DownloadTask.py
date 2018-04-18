# -*- coding: utf-8 -*-
from pixivapi.PixivUtils import DictObj

TASK_TYPE_ID = 1
TASK_TYPE_URL = 2
TASK_TYPE_SEARCH = 3
TASK_TYPE_SEARCH_API = 4
TASK_TYPE_RANKING = 5

DOWNLOAD_MODE_ID = 100
DOWNLOAD_MODE_URL = 101
DOWNLOAD_MODE_DETAIL = 102


class Task(DictObj):
    def __init__(self, task_type, download_mode, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.task_type = task_type
        self.download_mode = download_mode


if __name__ == '__main__':
    task = Task(TASK_TYPE_ID, **{"id": 1, 'path': "/", "url": "https://pixiv.net"})
    print (task.task_type)
    print (task.path)
    print (task.id)
    print (task.url)
    task.current_count = 100
    print (task.current_count)
