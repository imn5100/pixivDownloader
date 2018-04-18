# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread

from gui.DownloadTask import TASK_TYPE_ID, TASK_TYPE_SEARCH_API, TASK_TYPE_URL, TASK_TYPE_RANKING, TASK_TYPE_SEARCH, \
    DOWNLOAD_MODE_ID, DOWNLOAD_MODE_DETAIL, DOWNLOAD_MODE_URL
from pixiv.IllustrationDownloader import PAGE_LIMIT_CONTINUE
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
                # download
                if task.download_mode == DOWNLOAD_MODE_ID:
                    illu_file = self.downloader.download_all_by_id(task.id, task.path,
                                                                   p_limit=task.p_limit if task.has_key(
                                                                       'p_limit') else 0)
                elif task.download_mode == DOWNLOAD_MODE_URL:
                    illu_file = self.downloader.download_all_by_url(task.url, task.path)
                elif task.download_mode == DOWNLOAD_MODE_DETAIL:
                    illu_file = self.downloader.download_by_detail(task.illu, task.path, p_limit=task.p_limit)
                # callback
                if task.task_type == TASK_TYPE_ID and callback:
                    msg = CommonUtils.build_callback_msg(illu_file, id=str(task.id))
                    callback(msg)
                elif task.task_type == TASK_TYPE_URL and callback:
                    msg = CommonUtils.build_callback_msg(illu_file, url=str(task.url))
                    callback(msg)
                elif callback:
                    if illu_file:
                        if illu_file != PAGE_LIMIT_CONTINUE:
                            callback(
                                "%s:%s\nFile:%s\n\n" % (task.get_from + " get", task.illu.get('id'), illu_file))
                    else:
                        callback(
                            "%s:%s\nFile:%s\n\n" % (task.get_from + " get", task.illu.get('id'), 'Download Fail'))
            except Exception as e:
                print ("error", e)
            finally:
                queue.task_done()
                print ("Current Task Number:" + str(queue.qsize()))
                if callback and task and task.has_key('all_count') and task.all_count > 0:
                    if illu_file:
                        current_count = task.current_count.getAndInc()
                        if current_count + 1 == task.all_count:
                            afterEndCallback(task, callback)


def afterEndCallback(task, callback):
    if task.task_type == TASK_TYPE_SEARCH or task.task_type == TASK_TYPE_SEARCH_API:
        callback("***%s***\n%s\n\n" % ("Search:" + task.title, "The download task is complete",))
    if task.task_type == TASK_TYPE_RANKING:
        callback("***%s***\n%s\n\n" % (task.title, "The download task is complete",))
