import tkinter as tk
from io import BytesIO
from math import floor
from tkinter import *

import PIL
from PIL import Image, ImageTk
from dbase import *
from FileBase import *

db = Database()
db.createTable()

files = Filebase()
files.createTable()

BGC = "#123456"
root = tk.Tk()

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


def change_i():
    if sound_btn.image == icon:
        #start_recording()

        sound_btn.config(image=icon2)
        sound_btn.image = icon2
        im.show()
    else:
        #stop_recording()

        sound_btn.config(image=icon)
        sound_btn.image = icon

def resize(event):
    global window_width, window_height, ncols
    if (window_width != event.width) and (window_height != event.height):
        window_width, window_height = event.width,event.height
        print(f"The width of Toplevel is {window_width} and the height of Toplevel is {window_height}")
        ncols = window_width %128
        reGrid()


def reGrid():
    root.grid_forget()
    for iteration, x in enumerate(buttonArray):
        x.grid(row=floor(iteration / ncols) + 1, column=iteration % ncols)

window_width, window_height ,ncols= 0, 0, 1


















#
#
# im = PIL.Image.open("peach.jpg")
# print(im.filename)
#
# im.thumbnail((128, 128), Image.ANTIALIAS)
#
# icon = PIL.ImageTk.PhotoImage(im)
# icon2 = PhotoImage(file='smile.png')
#
# sound_btn = tk.Button(root, image=icon,relief=FLAT,command=change_i )
# sound_btn.image = icon
# sound_btn.grid(row=0, column=1)
#


tk.Label(root, text="Inside!", font=('Helvetica', 18, "bold")).grid(row=0, column=0)
filesarray = files.search_files_from_user((2,))
buttonArray = []
for iteration, x in enumerate(filesarray):
    im = stream_toImage(x[3])
    im.thumbnail((128, 128), Image.ANTIALIAS)
    icon = PIL.ImageTk.PhotoImage(im)

    icon = generate_thumbnail(x[3])

    sound_btn = tk.Button(root, image=icon, relief=FLAT, command=lambda lan=x: stream_toImage(lan[3]).show())
    sound_btn.image = icon
    buttonArray.append(sound_btn)
    sound_btn.grid(row=floor(iteration/ncols)+1, column=iteration % ncols)
    print(iteration)


a=root.winfo_reqheight()
b=root.winfo_reqwidth()
print("hei",a)
print('b', b)

root.bind("<Configure>", resize)
root.mainloop()