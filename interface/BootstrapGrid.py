from tkinter import ttk

# from HooverInfo import HoverInfo
from HooverInfo import HoverInfo

try:
    import Tkinter as tk
except:
    import tkinter as tk

from io import BytesIO

import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage

BGC = "#123456"


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=BGC)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        s = ttk.Style()
        s.configure('BGC.TFrame', background=BGC)
        self.scrollable_frame = ttk.Frame(self.canvas, style='BGC.TFrame')
        self.columns = 0
        self.selected_cards = list()
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.bind('<Configure>', self.regrid)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def regrid(self, event=None):
        grid_width = self.winfo_width()
        slaves = self.scrollable_frame.grid_slaves()
        slaves_width = slaves[1].winfo_width()
        cols = grid_width // slaves_width
        if (cols == self.columns) | (cols == 0):  # if the column number has not changed, abort
            return
        for i, slave in enumerate(reversed(slaves)):
            slave.grid_forget()
            slave.grid(row=i // cols, column=i % cols)
        self.columns = cols


class ImageCard(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, bd=1, relief=tk.RAISED, **kwargs)
        self.configure(width=300)
        self.file_id = tk.IntVar()
        self.image = tk.Button()
        self.check = tk.BooleanVar()
        self.config(bg='#123456')

    def add_button(self, x):
        icon = generate_thumbnail(x[3])
        self.file_id = x[0]
        self.image = tk.Button(self, image=icon, relief=tk.FLAT, height=130, width=130, pady=2, padx=2,bg='#123456',
                          command=lambda lan=x: stream_toImage(lan[3]).show())
        self.image.image = icon
        self.image.pack()

        return self

    def add_file_name(self, filename):
        #tk.Checkbutton(self, text=filename, variable=self.check, width=12, anchor='w',
        #                command=lambda lan=self.check: self.toggle(lan.get())).pack(side=tk.LEFT)
        tk.Checkbutton(self, text=filename, variable=self.check, width=12, anchor='w',bg=BGC, fg="grey",
                       command=lambda lan=self.check: toggle2(self,self.master.master.master, lan.get())).pack(side=tk.LEFT)
        #self.hover = HoverInfo(self, filename)
        return self

    def add_file_id(self, fileid):
        self.file_id = fileid
        return self

    def toggle(self, tf):
        if tf:
            self.config(bg='#123456')
        else:
            self.config(bg='#654321')
        self.master.selected

def toggle2(button :ImageCard ,master :ScrollableFrame, tf):
    if tf:
        master.selected_cards.append(button.file_id)
    else:
        master.selected_cards.remove(button.file_id)

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
