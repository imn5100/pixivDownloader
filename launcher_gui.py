# -*- coding: utf-8 -*-
from Tkinter import Tk

import sys

from gui.DownloaderGUI import PixivDownloadFrame, LogRedirection

if __name__ == '__main__':
    root = Tk()
    frame = PixivDownloadFrame(root)
    sys.stdout = LogRedirection(frame.print_text)
    root.mainloop()
