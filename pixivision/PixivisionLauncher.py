# -*- coding: utf-8 -*-
import threading

from pixiv_config import *
from pixivision.ImageDownload import ImageDownload, IlluDownloadThread


def start(url, save_path=IMAGE_SVAE_BASEPATH, quality=1, success_callback=None, fail_callback=None):
    topics = ImageDownload.get_pixivision_topics(url, save_path)
    ts = []
    for topic in topics:
        if topic.has_key("save_path"):
            t = IlluDownloadThread(topic.href, topic.save_path, quality).register_hook(
                success_callback=success_callback, fail_callback=fail_callback)
            t.start()
            ts.append(t)
    for t in ts:
        t.join()


class PixivisionLauncher(threading.Thread):
    def run(self):
        start(self.url, save_path=self.save_path, quality=self.quality, success_callback=self.success,
              fail_callback=self.fail)

    def __init__(self, url, save_path=IMAGE_SVAE_BASEPATH, quality=1):
        threading.Thread.__init__(self, name="PisivisionLauncher_" + url)
        self.url = url
        self.save_path = save_path
        self.quality = quality
        self.success = None
        self.fail = None

    def register_hook(self, success_callback=None, fail_callback=None):
        if success_callback:
            self.success = success_callback
        if fail_callback:
            self.fail = fail_callback
