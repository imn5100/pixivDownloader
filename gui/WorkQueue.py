# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread

from pixiv import PixivImageDownloader


class PixivQueue(object):
    def __init__(self, callback=None):
        self.queue = Queue()
        self.worker = Thread(target=PixivQueue.worker_run, args=(self.queue, callback))

    def run(self):
        self.worker.daemon = True
        self.worker.start()
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
                        if illu_file:
                            msg = "{\nId:" + str(task.get('id')) + "\nFile:" + illu_file + "\n}\n"
                        else:
                            msg = "{\nId:" + str(task.get('id')) + "\nFile:Download Fail\n}\n"
                        callback(msg)
                elif task.has_key('url') and task.has_key('path'):
                    illu_file = PixivImageDownloader.download_all_by_url(task.get('url'), task.get('path'))
                    if callback:
                        if illu_file:
                            msg = "{\nUrl:" + str(task.get('url')) + "\nFile:" + illu_file + "\n}\n"
                        else:
                            msg = "{\nUrl:" + str(task.get('url')) + "\nFile:Download Fail\n}\n"
                        callback(msg)
            except Exception, e:
                print ("error", e)
            finally:
                queue.task_done()
