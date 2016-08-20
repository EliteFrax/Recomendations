# Plugins module for LashProgram
from Tkinter import *
import os


def QuitProgram(program):
    if not 'normal' == program.state():
        return 0
    timer = 100
    size = program.winfo_geometry()
    w0, h0, x, y = map(int, size.replace("+", "x").strip().split("x"))
    while True:
        # Exit Animation
        # get actual size
        program.update()
        w, h = program.winfo_width(), program.winfo_height()

        ww = w / 1.1
        hh = h / 1.1
        dx = (w0 - ww) / 2.0
        dy = (h0 - hh) / 2.0
        xx = x + dx
        yy = y + dy

        ww, hh, xx, yy = map(int, (ww, hh, xx, yy))
        program.geometry("{}x{}+{}+{}".format(ww, hh, xx, yy))
        timer -= 1
        if (h <= 1) or timer < 0:
            break
    os._exit(1)
