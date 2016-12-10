# -*- coding: utf-8 -*-
import threading

from pixiv_config import *
from pixivision.ImageDownload import ImageDownload, IlluDownloadThread


def start(url, save_path=IMAGE_SVAE_BASEPATH, quality=1):
    topics = ImageDownload.get_pixivision_topics(url, save_path)
    ts = []
    for topic in topics:
        t = IlluDownloadThread(topic.href, topic.save_path, quality)
        t.start()
        ts.append(t)
    for t in ts:
        t.join()


class PixivisionLauncher(threading.Thread):
    def run(self):
        start(self.url, save_path=self.save_path, quality=self.quality)

    def __init__(self, url, save_path=IMAGE_SVAE_BASEPATH, quality=1):
        threading.Thread.__init__(self, name="PisivisionLauncher_" + url)
        self.url = url
        self.save_path = save_path
        self.quality = quality


