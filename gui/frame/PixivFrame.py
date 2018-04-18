# -*- coding: utf-8 -*-
from Tkinter import Frame


class PixivFrame(Frame):
    def __init__(self, master=None, name=None):
        Frame.__init__(self, master)
        self.name = name
        self.frames = None

    def set_frames(self, frames):
        self.frames = frames
        return self

    def switch(self):
        self.grid(row=1, columnspan=2)
        for frame in self.frames:
            if frame != self:
                frame.grid_forget()
