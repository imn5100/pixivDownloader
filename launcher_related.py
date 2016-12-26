# -*- coding: utf-8 -*-
import os
from Queue import Queue
from threading import Thread

from pixivapi.PixivApi import PixivApi
from pixivapi.PixivUtils import parse_json
from pixivision.PixivisionDownloader import HtmlDownloader


def consumer_download_work(queue, save_path):
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
            print("download Fail  remove id" + str(illust.id))
            print(e)
            continue
        finally:
            queue.task_done()


def producer_put_work(related, queue):
    if related and related.has_key("illusts"):
        for illust in related.illusts:
            queue.put(illust)


def relate_illust(seed, depth=2, image_path='imageDownload'):
    queue = Queue()
    save_path = (image_path + "/related_%s") % str(seed)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # 启动消费者下载器
    for i in range(3):
        t = Thread(target=consumer_download_work, args=(queue, save_path))
        t.daemon = True
        t.start()

    related = PixivApi.illust_related(seed)
    # 解析返回json串，将下载url放入队列
    producer_put_work(related, queue)
    if related.has_key("next_url"):
        url = related.next_url
    else:
        print("There is no next URL，（无法查询到关联作品）")
        return
    count = 1
    while True:
        # 间隔时间
        # time.sleep(2)
        resp = HtmlDownloader.download(url)
        related2 = parse_json(resp)
        if related.has_key("next_url"):
            url = related.next_url
        else:
            print("There is no next URL，（没有查询到关联作品）")
            break
        print("Depth :" + str(count) + " Associated illust:" + str(len(related2.illusts)))
        print("Next URL:" + related2.next_url)
        producer_put_work(related2, queue)
        # 需要到达的深度
        if count == depth:
            print("producer completed!")
            break
        count += 1
    queue.join()


if __name__ == '__main__':
    depth = raw_input(
            "Please enter a number  as the depth of the associated download:\n请输入关联下载的深度。\
            (每次拉取的关联作品会作为下一拉取的关联的种子，深度即向下关联拉取的次数,每次向下关联越拉取20-30副插画)\n")
    seed = int(raw_input(
            "Please enter a Pixiv illustration ID as the seed of the associated download:\n请输入Pixiv插画id作为关联下载的种子\n"))
    image_path = raw_input("Please enter illustration save path，请输入插画存储位置\n")
    try:
        depth = int(depth)
    except:
        depth = 2
    relate_illust(seed, depth, image_path)
