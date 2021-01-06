# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
from io import BytesIO


import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage



import MainWindow as MW
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import Label,  FLAT,  Menu



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

        # create the real Frame for images
        image_list_frame = tk.Frame(self, height=100, width=100, bg=BGC, borderwidth=2)
        image_list_frame.pack()
        # Create WidgetWrapper
        # state = "disabled" is to disable text from being input by user
        # cursor = "arrow" is to ensure when user hovers, the arrow is displayed
        widget_wrapper = tk.Text(image_list_frame, wrap="char", borderwidth=0, highlightthickness=0, state="disabled",
                                 cursor="arrow", bg=BGC)
        widget_wrapper.pack(fill="both", expand=True)

        # fill with images
        files_array = files.search_files_from_user((2,))
        for iteration, x in enumerate(files_array):
            icon = generate_thumbnail(x[3])
            sound_btn = tk.Button(image_list_frame, image=icon, padx=20, relief= FLAT,
                                  command=lambda lan=x: stream_toImage(lan[3]).show())
            sound_btn.image = icon
            self.additem(widget_wrapper, sound_btn)
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
