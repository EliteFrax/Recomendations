# global imports
from Tkinter import *
import ttk
import os

# own imports
import Plugins

# create master and main widget
master = Tk()
program_name = "Program Name"
master.wm_title(program_name)
master.overrideredirect(1)

# frame_time, used to control timers by doing frame_time % <timer> == 0
# can also be used to know the ammount of frames the program has played
frame_time = 0
smooth_value = 0
global_timer = 0
updated = False
new_created = True
last_geometry = Plugins.ProgramGetSize(master)
new_geometry = last_geometry

#colors
program_bg = "#2980b9"
program_border = "#1c567d"
program_border_dark = "#123a54"

#widgets
program_bg_clear_fg = "#2980b9"
program_bg_dark_fg = "#3498db"

program_fg_clear_bg = "#2c3e50"
program_fg_dark_bg = "#34495e"

#set program window background color
master["bg"]=program_bg
main_border=Frame(master, bg=program_border)
top_bar = Frame(main_border, bg=program_border)
#move window with top_bar if clicked
top_bar.bind("<Button-1>", lambda x: Plugins.ProgramDragWithMouse(master, x))

#functions
def ProgramEnd(frame = None):
    os._exit(1)

close_button = Button(top_bar, text="x", command=lambda: ProgramEnd(),
                      bg=program_border_dark, fg="white", bd=0,
                      highlightthickness=0)

def main(status = "Login"):
    global last_geometry, new_geometry, updated, new_created
    
    main_frame = Frame(main_border, bg=program_bg)
    program_status = status
    #Misc Functions
    def UnbindWheel(widget):
        widget.bind("<MouseWheel>", DoNothing) # windows and mac
        widget.bind("<Button-4>", DoNothing) # linux specific
        widget.bind("<Button-5>", DoNothing) # linux specific
        
    def DoNothing(event):
            return "break"

    #constants and program-based value
    user_list = {
        0: "Juan Perez",
        1: "Lucas Rojas",
        2: "Rodrigo Mesa",
        3: "Pedro Palma",
        4: "Amarando Cortez",
        5: "Javier Astorga",
        6: "Ignacio Rivero",
        7: "Carlos Gomez",
        8: "Federico Santamaria",
        9: "Antonio Rios",
        10: "Cesar Bustamante",
        11: "Esteban Soto",
        12: "Marisol Tapia",
    }
    user_list_length = len(user_list.keys())

    # no matter the program_status, there is a menu, if a program_status 
    # needs tohide it, there is a config for it
    menu0 = Menu(main_frame)
    #master.config(menu=menu0)

    def hello(): pass

    filemenu = Menu(menu0, tearoff=0)
    filemenu.add_command(label="Open", command=hello)
    filemenu.add_command(label="Save", command=hello)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=lambda: ProgramEnd(main_frame))
    menu0.add_cascade(label="File", menu=filemenu)

    # setup widgets based on program_status
    if program_status == "Login":
        label0 = Label(main_frame, text="Bienvenido a", font=("Mono", 16),
                       bg=program_bg)
        label1 = Label(main_frame, text=program_name, font=("Mono", 24),
                       bg=program_bg)
        label2 = Label(main_frame, text="Elija su usuario de la lista:",
                       font=("Sans", 12), bg=program_bg)
        
        listbox0 = Listbox(main_frame, relief=FLAT, selectmode=SINGLE, bd=0,
                           highlightthickness=0)
        
        scale0 = Scale(main_frame, from_=0, to_=100, orient="vertical",
                       showvalue=0, borderwidth=0, sliderrelief=FLAT,
                       highlightcolor=program_bg, highlightthickness=0)
        
        bf = Frame(main_frame, bg=program_bg)
        bf_left = Frame(bf, bg=program_bg)
        bf_right = Frame(bf, bg=program_bg)
        
        button0 = Button(bf_left, text="Login", relief=FLAT,
                         command=lambda: ProgramSwitchMode("Loading"),
                         bg=program_bg, highlightthickness=0)
        button1 = Button(bf_right, text="Exit", relief=FLAT,
                         command=lambda: ProgramEnd(main_frame),
                         bg=program_bg, highlightthickness=0)
        
        label0.grid(row=0, padx=8)
        label1.grid(row=1, padx=8, pady=(0, 8))
        label2.grid(row=2, padx=8, sticky=W)
            
        listbox0.grid(row=3, padx=(8,26), pady=(12,4), sticky=W+E)
        scale0.grid(row=3, padx=(0, 8), pady=(12, 4), sticky=E+N+S)
        
        bf.grid(row=4, sticky=W+E)
        bf_left.pack(fill=BOTH, expand=YES, side=LEFT, padx=(8, 0), pady=4)
        bf_right.pack(fill=BOTH, expand=YES, side=RIGHT, padx=(0, 8), pady=4)

        button0.pack(fill=BOTH)
        button1.pack(fill=BOTH)
        
        UnbindWheel(listbox0)
        for user_id, user in user_list.items():
            listbox0.insert(END, str(user))
        for i in range(len(user_list)):
            #colour items based on modulo
            try:
                if i%2==0:
                    color = program_bg_clear_fg
                    color2 = program_fg_dark_bg
                else:
                    color = program_bg_dark_fg
                    color2 = program_fg_clear_bg
                listbox0.itemconfig(i, {'bg':color, "fg":color2})
            except:
                break
        
    elif program_status == "Loading":
        #design Loading screen
        label0 = Label(main_frame, text="Loading content...",
                       font=("Monospaced", 24), bg=program_bg)
        (animation0, 
        animation0_list, 
        animation0_len) = Plugins.GetAnimationFromGif(main_frame, "data/running.gif")
        
        animation0.config(bg=program_bg)
        label0.grid(row=0)
        animation0.grid(row=1, pady=8)

    elif program_status == "TopTen":
        label0 = Label(main_frame, text="Estas son las 10 peliculas\nrecomendadas para usted!",
                       font=("Serif", 16), bg=program_bg)
        data_frame = Frame(main_frame, bg=program_bg)
        count, count_list, count_len = Plugins.GetAnimationFromGif(main_frame, "data/countdown.gif") 
        count["bg"] = program_bg
        scale0 = Scale(main_frame, orient="horizontal", showvalue=0, relief=FLAT,
                       borderwidth=0, from_=0, to=9, sliderrelief=FLAT,
                       highlightthickness=0)

        label1 = Label(data_frame, text=" "*20, font=("Mono", 16), bg=program_bg)
        label2 = Label(data_frame, text="", font=("Serif", 12), bg=program_bg)
        label3 = Label(data_frame, text="", font=("Serif", 12), bg=program_bg)
        
        button0 = Button(main_frame, text="Volver Atras!",
                         command=lambda: ProgramSwitchMode("Login"),
                         highlightthickness=0)
        
        label0.grid(row=0, columnspan=2)
        label1.pack(fill=BOTH, padx=8)
        label2.pack(fill=X, padx=8)
        label3.pack(fill=X, padx=8)
        
        data_frame.grid(row=1, column=1, sticky=N+S+W+E)
        
        count.grid(row=1, padx=8)
        scale0.grid(row=2, sticky=W+E, padx=8)
        button0.grid(row=2, column=1, padx=8, pady=4, sticky=W+E)

    #allow for ProgramUpdateWidgets to modify widgets properties
    updated = True
    
    #UpdateStep function
    def ProgramUpdateWidgets():
        global frame_time, global_timer, smooth_value
        # get program size
        program_width, program_height = master.winfo_width(), master.winfo_height()
        frame_time += 1
        #master.update()
        master.geometry("")
        
        #dont update if no widgets exists
        if updated == False:
            return 0
        try:
            if program_status == "None":
                ProgramEnd(main_frame)
                
            if program_status == "Login":
                #set scale0 <to> based on listbox0 length
                user_list_length = len(user_list)
                listbox0_max = max(user_list_length - int(listbox0["height"]), 0)
                scale0.config(to=listbox0_max, resolution=0.01)
                
                #set listbox position based on scale
                listbox0_y = int(round(scale0.get() ))
                listbox0.yview(listbox0_y)
                
            elif program_status == "Loading":
                animation0.config(image=animation0_list[(frame_time/400)%animation0_len])
                if frame_time%100 == 0:
                    global_timer += 1
                if global_timer >= 200:
                    global_timer = 0
                    ProgramSwitchMode("TopTen")
                
            elif program_status == "TopTen":
                tenth = (count_len)/10.0
                value = tenth * float(scale0.get())
                smooth_value += (value - smooth_value)/1000.0
                
                count.config(image=count_list[int(smooth_value%count_len)])
                
                label1.config(text=str("Movie Number "+str(10-scale0.get())+": ").center(20))
                #label1.config(text="frames: "+str(count_len))
                label2.config(text="sframe: "+str(round(smooth_value,2)))
                label3.config(text="frame: "+str(value))
        except:
            return 0
        
    def ProgramSwitchMode(mode="Loading"):
        global updated, last_geometry
        last_geometry = Plugins.ProgramGetSize(master)
        main_frame.destroy()
        updated = False
        main(mode)
        

    # show main_frame, no longer available to edit
    close_button.pack(side=RIGHT)
    top_bar.pack(fill=BOTH)
    main_frame.pack(fill=BOTH, padx=4, pady=(0,4))
    main_border.pack(fill=BOTH)
    # resize program
    master.update()
    master.geometry("")
    master.update()
    if new_created:
        last_geometry = Plugins.ProgramGetSize(master)
        new_created = False
    else:
        master.update()
        new_geometry = Plugins.ProgramGetSize(master)
        Plugins.ProgramResizeSmooth(master, last_geometry, new_geometry)
    #print last_geometry, new_geometry
    
    # main loop
    master.resizable(width=False, height=False)
    master.protocol("WM_DELETE_WINDOW", lambda: ProgramEnd(master))
    while True:
        master.after(1000/60, lambda: ProgramUpdateWidgets())
        master.update()

if __name__ == "__main__":
    main("Login")
