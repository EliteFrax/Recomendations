# Plugins. Por LashPollo
from Tkinter import *
import os

def ObtenerAnimacionDeGif(parent, filename, wgtype="texto"):
    animacion = []
    indice = 0
    while True:
        try:
            animacion.append(PhotoImage(file=filename, format="gif -index {0}".format(indice)))
            indice += 1
        except:
            break
    if not animacion:
        return 0,0,0
    if wgtype=="texto":
        wg = Label(parent, image=animacion[0],highlightthickness=0)
    elif wgtype=="button":
        gw = Button(parent, image=animacion[0],bd=0,highlightthickness=0)
    return wg, animacion, len(animacion)

def ObtenerGeometriaPrograma(maestro):
    size = (maestro.winfo_width(), maestro.winfo_height())
    return map(int, size)

def EscalarProgramaSuavemente(maestro, last_size, new_size):
    new_w, new_h = last_size[0:2]
    timer = 0
    while True:
        maestro.update()
        new_w += (new_size[0]-new_w)/5.0
        new_h += (new_size[1]-new_h)/5.0
        
        maestro.geometry("{0}x{1}".format(int(new_w), int(new_h)))
        timer += 1
        if timer >= 500:
            break
    maestro.update()

def ProgramDragWithMouse(maestro, event):
    maestro.update()
    pos_actual = maestro.winfo_geometry().replace("+","x").strip().split("x")
    pos_actual = map(int, pos_actual)[2:4]
    
    rel_x = maestro.winfo_pointerx() - pos_actual[0]
    rel_y = maestro.winfo_pointery() - pos_actual[1]
    new_x, new_y = pos_actual
    
    xx = event.x
    yy = event.y
    
    dragging = [True]
    
    def TerminarLoop(event):
        dragging[0] = False
        
    while dragging[0]:
        maestro.update()
        pos = (maestro.winfo_pointerx(), maestro.winfo_pointery())
        
        new_x += ((pos[0]-rel_x) - new_x) / 10.0
        new_y += ((pos[1]-rel_y) - new_y) / 10.0
    
        maestro.geometry("+{0}+{1}".format(int(new_x), int(new_y)))
        
        maestro.bind("<ButtonRelease-1>", TerminarLoop)
    maestro.unbind("<ButtonRelease-1>")
    
