# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import Label, FLAT, Menu, BOTH
from io import BytesIO
import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage

import MainWindow as MW
import BootstrapGrid


from dbase import *
from FileBase import *
db = Database()
db.createTable()

files = Filebase()
files.createTable()

BGC = "#123456"


class AppViewPage(tk.Frame):

    def men_bar(self):
        menubar = Menu(self)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")

        file.add_separator()
        file.add_command(label="Close Session", command=lambda: self.master.switch_frame(MW.StartPage))
        file.add_command(label="Exit", command=self.master.quit)

        menubar.add_cascade(label="File", menu=file)
        edit = Menu(menubar, tearoff=0)
        edit.add_command(label="Undo")

        edit.add_separator()

        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Paste")
        edit.add_command(label="Delete")
        edit.add_command(label="Select All")

        menubar.add_cascade(label="Edit", menu=edit)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)
        self.master.config(menu=menubar)
        return

    def additem(self, widgetWrapper, item):
        widgetWrapper.window_create("end", window=item)  # Put it inside the widget wrapper (the text)

    def __init__(self, master):
        # configure frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BGC)
        self.master.resizable(1, 1)

        self.men_bar()

        # headers
        tk.Label(self, text="PorkinVault", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        hello_label = Label(self, text="HELOOO MODAFOKA", bg=BGC, fg="white")
        hello_label.pack()


        frame = BootstrapGrid.AutoGrid(self,bg=BGC)
        frame.pack(expand=True, fil=BOTH)
        files_array = files.search_files_from_user((2,))
        #
        for iteration, x in enumerate(files_array):
            BootstrapGrid.ImageCard(frame).add_button(x).add_file_name(x[2]).grid()
            print(iteration)




def stream_toImage(stream) -> Image:
    stream = BytesIO(stream)
    im = Image.open(stream).convert("RGBA")
    stream.close()
    return im


def generate_thumbnail(xablau) -> PhotoImage:
    im = stream_toImage(xablau)
    im.thumbnail((128, 128), Image.ANTIALIAS)
    icon = PIL.ImageTk.PhotoImage(im)
    return icon
