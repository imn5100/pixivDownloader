# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread

from pixiv import PixivImageDownloader
from pixivapi.PixivApi import PixivApi
from utils import CommonUtils


class PixivQueue(object):
    def __init__(self, callback=None, thread_num=5):
        self.queue = Queue()
        self.workers = []
        self.thread_num = thread_num
        for i in range(1, thread_num + 1):
            self.workers.append(Thread(target=PixivQueue.worker_run, args=(self.queue, callback)))

    def run(self):
        for worker in self.workers:
            worker.daemon = True
            worker.start()
        self.queue.join()

    def add_work(self, task):
        self.queue.put(task)

    @classmethod
    def worker_run(cls, queue, callback):
        while True:
            try:
                task = queue.get()
                if not task:
                    continue
                if task.has_key('id') and task.has_key('path'):
                    illu_file = PixivImageDownloader.download_all_by_id(task.get('id'), task.get('path'))
                    if callback:
                        msg = CommonUtils.build_callback_msg(illu_file, id=str(task.get('id')))
                        callback(msg)
                elif task.has_key('path') and task.has_key('url'):
                    illu_file = PixivImageDownloader.download_all_by_url(task.get('url'), task.get('path'))
                    if callback:
                        msg = CommonUtils.build_callback_msg(illu_file, url=str(task.get('url')))
                        callback(msg)
                elif task.has_key('title') and task.has_key('url') and task.has_key('search_path'):
                    illu_file = PixivImageDownloader.download_illustration(task, task.get('search_path'), PixivApi,
                                                                           p_limit=task.get('p_limit'))
                    if callback and illu_file:
                        callback("{\n%s:%s\nFile:%s\n}\n" % ("search get", task.get('title'), illu_file))
            except Exception as e:
                print ("error", e)
            finally:
                queue.task_done()
                print ("Current Task Number:" + str(queue.qsize()))
