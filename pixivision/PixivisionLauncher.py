# -*- coding: utf-8 -*-
import threading

from pixiv_config import *
from pixivision.PixivisionTopicDownloader import ImageDownload, IlluDownloadThread
from utils.AtomicInteger import AtomicInteger


def start(url, save_path=IMAGE_SAVE_BASEPATH, downloader=None, success_callback=None, fail_callback=None):
    topics = ImageDownload.get_pixivision_topics(url, save_path)
    ts = []
    callback_params = {
        'all_count': len(topics),
        'current_count': AtomicInteger(),
        'url': url
    }
    for topic in topics:
        if topic.has_key("save_path"):
            t = IlluDownloadThread(topic.href, path=topic.save_path, downloader=downloader).register_hook(
                success_callback=success_callback, fail_callback=fail_callback, params=callback_params)
            t.start()
            ts.append(t)
    for t in ts:
        t.join()


class PixivisionLauncher(threading.Thread):
    def run(self):
        start(self.url, save_path=self.save_path, downloader=self.downloader, success_callback=self.success,
              fail_callback=self.fail)

    def __init__(self, url, save_path=IMAGE_SAVE_BASEPATH, downloader=None):
        threading.Thread.__init__(self, name="PisivisionLauncher_" + url)
        self.url = url
        self.save_path = save_path
        self.success = None
        self.fail = None
        self.downloader = downloader

    def register_hook(self, success_callback=None, fail_callback=None):
        if success_callback:
            self.success = success_callback
        if fail_callback:
            self.fail = fail_callback
        return self
