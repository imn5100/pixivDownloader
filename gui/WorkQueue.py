# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread

from gui.DownloadTask import TASK_TYPE_ID, TASK_TYPE_SEARCH_API, TASK_TYPE_URL, TASK_TYPE_RANKING, TASK_TYPE_SEARCH
from pixivapi.PixivUtils import PixivError
from utils import CommonUtils


class PixivQueue(object):
    def __init__(self, downloader, callback=None, thread_num=5):
        if not downloader:
            raise PixivError('You must set a downloader for the queue')
        self.downloader = downloader
        self.queue = Queue()
        self.workers = []
        self.thread_num = thread_num
        for i in range(1, thread_num + 1):
            self.workers.append(Thread(target=self.worker_run, args=(self.queue, callback)))

    def run(self):
        for worker in self.workers:
            worker.daemon = True
            worker.start()
        self.queue.join()

    def add_work(self, task):
        self.queue.put(task)

    def add_all_work(self, tasks):
        for task in tasks:
            self.queue.put(task)

    def worker_run(self, queue, callback):
        while True:
            try:
                task = queue.get()
                if not task:
                    continue
                illu_file = None
                if task.task_type == TASK_TYPE_ID:
                    illu_file = self.downloader.download_all_by_id(task.id, task.path)
                    if callback:
                        msg = CommonUtils.build_callback_msg(illu_file, id=str(task.id))
                        callback(msg)
                elif task.task_type == TASK_TYPE_URL:
                    illu_file = self.downloader.download_all_by_url(task.url, task.path)
                    if callback:
                        msg = CommonUtils.build_callback_msg(illu_file, url=str(task.url))
                        callback(msg)
                elif task.task_type == TASK_TYPE_SEARCH:
                    illu_file = self.downloader.download_illustration(task.illu, task.path, p_limit=task.p_limit)
                    if callback:
                        if illu_file:
                            callback("{\n%s:%s\nFile:%s\n}\n" % ("search get", task.illu.get('title'), illu_file))
                        else:
                            callback("{\n%s:%s\nFile:%s\n}\n" % ("search get", task.illu.get('url'), 'Download Fail'))
                elif task.task_type == TASK_TYPE_SEARCH_API:
                    illu_file = self.downloader.download_by_detail(task.illu, task.path, p_limit=task.p_limit)
                    if callback:
                        if illu_file:
                            callback("{\n%s:%s\nFile:%s\n}\n" % ("search get", task.illu.get('title'), illu_file))
                        else:
                            callback("{\n%s:%s\nFile:%s\n}\n" % ("search get", task.illu.get('id'), 'Download Fail'))
                elif task.task_type == TASK_TYPE_RANKING:
                    illu_file = self.downloader.download_by_detail(task.illu, task.path, p_limit=task.p_limit)
                    if callback:
                        if illu_file:
                            callback("{\n%s:%s\nFile:%s\n}\n" % ("ranking get", task.illu.get('title'), illu_file))
                        else:
                            callback("{\n%s:%s\nFile:%s\n}\n" % ("ranking get", task.illu.get('id'), 'Download Fail'))
            except Exception as e:
                print ("error", e)
            finally:
                if task and task.has_key('all_count') and task.all_count > 0:
                    if illu_file:
                        current_count = task.current_count.getAndInc()
                        if current_count + 1 == task.all_count:
                            callback("{\n%s:%s\nFile:%s\n}\n" % ("ranking get", task.illu.get('id'), 'Download Fail'))
                queue.task_done()
                print ("Current Task Number:" + str(queue.qsize()))
