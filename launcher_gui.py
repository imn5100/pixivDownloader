# -*- coding: utf-8 -*-
from Tkinter import Tk

from gui.LoginFrame import LoginFrame

if __name__ == '__main__':
    root = Tk()
    frame = LoginFrame(root)
    root.mainloop()
