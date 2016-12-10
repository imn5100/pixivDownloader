# -*- coding: utf-8 -*-
import logging
import sys

formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stderr)
download_fail_logger = logging.getLogger("Download_Fail")
download_fail_logger.setLevel(logging.ERROR)
download_fail_logger.addHandler(file_handler)
download_fail_logger.addHandler(stream_handler)


def error_log(fmt, *args):
    download_fail_logger.error(fmt, *args)
