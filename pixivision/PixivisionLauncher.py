# -*- coding: utf-8 -*-
import threading

from pixiv_config import *
from pixivision.ImageDownload import ImageDownload, IlluDownloadThread


class PixivisionLauncher(threading.Thread):
    def __init__(self, url, save_path=IMAGE_SVAE_BASEPATH, quality=1):
        threading.Thread.__init__(self, name="PisivsionLauncher_" + url)
        self.url = url
        self.save_path = save_path
        self.quality = quality

    def run(self):
        topics = ImageDownload.get_pixivision_topics(self.url, self.save_path)
        ts = []
        for topic in topics:
            t = IlluDownloadThread(topic.href, topic.save_path, self.quality)
            t.start()
            ts.append(t)
        for t in ts:
            t.join()
