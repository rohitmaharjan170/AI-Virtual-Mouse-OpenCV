from tkinter import *
import os

root = Tk()
root.geometry("370x450")  # set width and height of frame
root.configure(background="#66ff33")  # adding background color
root.minsize(370, 450)  # setting minimum size of frame
root.maxsize(370, 450)  # setting maximum size of frame
root.title("Ai Virtual Mouse")  # setting title


def run():  # function to run live Ai virtual mouse
    os.system("python AiVirtualMouseProject.py")


def HandTrackingModule():  # function to run HandTrackingModule
    os.system("python HandTrackingModule.py")


def quit():  # function to exit
    sys.exit()
    root.destroy()


# Label text
labeltxt = Label(text="Ai Virutal Mouse Controller", font=("comicsans", 18, "bold"), pady=30, bg="#66ff33",
                 fg="#000000")
labeltxt.pack()

# button to execute run function
start = Button(root, text="Live Ai Virtual mouse", width=20, command=run, font="30", borderwidth=0)
start.pack(pady=5)

# button to halt run function
# stop = Button(root, text="Stop Ai Virtual mouse", width=20, command=exit, font="30", borderwidth=0)
# stop.pack(pady=5)

# button to exit code
exitt = Button(root, text="Exit", width=20, font="30", command=quit, borderwidth=0, )
exitt.pack(pady=5)

root.mainloop()
