# Tkinter Application Module
# uses Plugins in some commands, to use fancy animations

from Tkinter import *
import os
import Plugins

program_status = "None"


def RunApplicationStatus(status="Login"):
    global program_status
    program_status = status
    main()


def main():
    # define master widget
    program = Tk()
    master = Frame(program, bg="red").grid(row=0)

    program.update()

    # Get usernames
    list_of_users = {
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

    # Create UI

    # Define control functions
    def UnbindWheel(widget):
        widget.bind("<MouseWheel>", NoOp)
        widget.bind("<Button-4>", NoOp)
        widget.bind("<Button-5>", NoOp)

    def NoOp(event):
        return "break"

    if program_status == "Login":
        label_0 = Label(master, text="Welcome to",
                        font=("Liberation Sans", 16))
        label_1 = Label(master, text="ProgramName!",
                        font=("Liberation Sans", 24))
        label_2 = Label(master, text="Choose your username",
                        font=("Liberation Sans", 11))
        label_3 = Label(master, text="from the list below:",
                        font=("Liberation Sans", 11))

        # combobox_0 = Plugins.ComboBoxDict(master, list_of_users)
        combobox_0 = Listbox(master, relief=FLAT, selectmode=SINGLE,
                             bd=0)
        slider_0 = Scale(master, from_=0, to=100, orient=VERTICAL,
                         showvalue=0, borderwidth=0)

        button_frame = Frame(master)
        button_frame_left = Frame(button_frame)
        button_frame_right = Frame(button_frame)

        button_0 = Button(button_frame_left, text="Login")
        button_1 = Button(button_frame_right, text="Cancel",
                          command=lambda: Plugins.QuitProgram(program))

        # apply grid to widgets
        label_0.grid(row=0, padx=8)
        label_1.grid(row=1, padx=8, pady=(0, 8))
        label_2.grid(row=2, padx=8, sticky=W)
        label_3.grid(row=3, padx=8, sticky=W)

        combobox_0.grid(row=4, padx=(8, 24), pady=(12, 4), sticky=W + E)
        slider_0.grid(row=4, padx=(0, 8), pady=(12, 4), sticky=E + N + S)

        button_frame.grid(row=5, sticky=W + E)
        button_frame_left.pack(fill=BOTH, expand=YES, side=LEFT,
                               padx=(8, 0), pady=4)
        button_frame_right.pack(fill=BOTH, expand=YES, side=RIGHT,
                                padx=(0, 8), pady=4)

        button_0.pack(fill=BOTH)
        button_1.pack(fill=BOTH)

        # configuration variables
        a = len(list_of_users.keys())
        combobox_0_max = max(a - int(combobox_0["height"]), 0)
        slider_0.config(to=combobox_0_max, resolution=0.01)
        UnbindWheel(combobox_0)

        # manage widgets
        # combobox users append
        for user_id, user in list_of_users.items():
            combobox_0.insert(END, str(user))

    # update function
    def update():
        if program_status == "Login":
            combobox_0_y = int(round(slider_0.get()))
            combobox_0.yview(combobox_0_y)

    # Tk main loop
    # program.overrideredirect(True)
    program.resizable(width=False, height=False)
    program.protocol("WM_DELETE_WINDOW", lambda: Plugins.QuitProgram(program))
    while True:
        program.after(1, update)
        program.update()

if __name__ == "__main__":
    RunApplicationStatus("Login")
