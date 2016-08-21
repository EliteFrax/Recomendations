# Plugins module
from Tkinter import *
import os

def GetAnimationFromGif(parent, filename, wgtype="label"):
    animation = []
    index = 0
    while True:
        try:
            animation.append(PhotoImage(file=filename, format="gif -index {0}".format(index)))
            index += 1
        except:
            break
    if not animation:
        return 0
    if wgtype=="label":
        wg = Label(parent, image=animation[0],highlightthickness=0)
    elif wgtype=="button":
        gw = Button(parent, image=animation[0],bd=0,highlightthickness=0)
    return wg, animation, len(animation)

def ProgramGetSize(master):
    size = (master.winfo_width(), master.winfo_height())
    return map(int, size)

def ProgramResizeSmooth(master, last_size, new_size):
    new_w, new_h = last_size[0:2]
    timer = 0
    while True:
        master.update()
        new_w += (new_size[0]-new_w)/5.0
        new_h += (new_size[1]-new_h)/5.0
        
        master.geometry("{0}x{1}".format(int(new_w), int(new_h)))
        timer += 1
        if timer >= 500:
            break
    master.update()

def ProgramDragWithMouse(master, event):
    master.update()
    actual_pos = master.winfo_geometry().replace("+","x").strip().split("x")
    actual_size = map(int, actual_pos)[0:2]
    actual_pos = map(int, actual_pos)[2:4]
    
    rel_x = master.winfo_pointerx() - actual_pos[0]
    rel_y = master.winfo_pointery() - actual_pos[1]
    
    xx = event.x
    yy = event.y
    
    dragging = [True]
    
    def end_all(event):
        dragging[0] = False
        
    while dragging[0]:
        master.update()
        pos = (master.winfo_pointerx(), master.winfo_pointery())
        
        new_x = pos[0]-rel_x
        new_y = pos[1]-rel_y
    
        master.geometry("+{0}+{1}".format(new_x, new_y))
        
        master.bind("<ButtonRelease-1>", end_all)
    master.unbind("<ButtonRelease-1>")
    
