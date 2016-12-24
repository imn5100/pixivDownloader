# -*- coding: utf-8 -*-
import os
from Queue import Queue
from threading import Thread

import redis

from pixiv_config import REDIS_IP, REDIS_PORT
from pixivapi.PixivApi import PixivApi
from pixivapi.PixivUtils import parse_json
from pixivision.PixivisionDownloader import HtmlDownloader
from utils.RedisFilter import RedisFilter


def consumer_download_work(queue, save_path, i_filter):
    while True:
        try:
            illust = queue.get()
            if illust.page_count == 1:
                try:
                    url = illust.meta_single_page.original_image_url
                except:
                    url = illust.image_urls.large
            else:
                url = illust.image_urls.large
            extension = os.path.splitext(url)[1]
            image_save_path = save_path + "/p_%s%s" % (illust.id, extension)
            PixivApi.download(url, path=image_save_path)
            print("download " + image_save_path + "\n")
        except Exception, e:
            i_filter.remove(illust.id)
            print("download Fail  remove id" + str(illust.id))
            print(e)
            continue
        finally:
            queue.task_done()


def producer_put_work(related, queue, i_filter):
    if related and related.has_key("illusts"):
        for illust in related.illusts:
            if not i_filter.is_contained(illust.id):
                # 加入下载队列
                queue.put(illust)
                i_filter.add(illust.id)
            else:
                print("contained:" + str(illust.id))
                continue


def relate_illust(seed):
    queue = Queue()
    r = redis.Redis(REDIS_IP, REDIS_PORT)
    i_filter = RedisFilter(r, 5, "setFilter2:PixivRelated")
    save_path = "E:/imageDownLoad/related_%s" % str(seed)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # 启动消费者下载器
    for i in range(3):
        t = Thread(target=consumer_download_work, args=(queue, save_path, i_filter))
        t.daemon = True
        t.start()

    related = PixivApi.illust_related(seed)
    # 解析返回json串，将下载url放入队列
    producer_put_work(related, queue, i_filter)
    url = related.next_url
    count = 1
    while True:
        # 间隔时间
        # time.sleep(2)
        resp = HtmlDownloader.download(url)
        related2 = parse_json(resp)
        url = related2.next_url
        print("Depth :" + str(count) + " Associated illust:" + str(len(related2.illusts)))
        print("Next URL:" + related2.next_url)
        producer_put_work(related2, queue, i_filter)
        # 需要到达的深度
        if count == 2:
            print("producer completed!")
            break
        count += 1
    queue.join()


if __name__ == '__main__':
    seed = int(raw_input(
            "Please enter a Pixiv illustration ID as the seed of the associated download:\n请输入Pixiv插画id作为关联下载的种子\n"))
    relate_illust(seed)
