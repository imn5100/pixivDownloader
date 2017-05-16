# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread

from pixivision.ImageDownload import ImageDownload


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
                    illu_file = ImageDownload.download_image_byid(task.get('id'), task.get('path'))
                    if callback and illu_file: callback(illu_file, id=task.get('id'))
                elif task.has_key('url') and task.has_key('path'):
                    illu_file = ImageDownload.download_byurl(task.get('url'), task.get('path'))
                    if callback and illu_file: callback(illu_file, url=task.get('url'))
            except Exception, e:
                print ("error", e)
            finally:
                queue.task_done()
