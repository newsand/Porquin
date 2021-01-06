try:
    import Tkinter as tk
except:
    import tkinter as tk

from io import BytesIO

import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage


class AutoGrid(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.columns = None
        self.bind('<Configure>', self.regrid)

    def regrid(self, event=None):
        grid_width = self.winfo_width()
        slaves = self.grid_slaves()
        slaves_width = max(slave.winfo_width() for slave in slaves)
        cols = grid_width // slaves_width
        if (cols == self.columns) | (cols == 0):  # if the column number has not changed, abort
            return
        for i, slave in enumerate(reversed(slaves)):
            slave.grid_forget()
            slave.grid(row=i // cols, column=i % cols)
        self.columns = cols


class ImageCard(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, bd=5, relief=tk.RAISED, **kwargs)

    def add_button(self, x):
        icon = generate_thumbnail(x[3])
        sound_btn = tk.Button(self, image=icon, relief=tk.FLAT, height=130, width=130, pady=2, padx=2,
                              command=lambda lan=x: stream_toImage(lan[3]).show())
        sound_btn.image = icon
        sound_btn.pack()
        return self

    def add_file_name(self, filename):
        tk.Label(self, text=filename).pack(pady=10)
        return self



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


# example of using autogrid
# def main():
#     root = tk.Tk()
#     frame = AutoGrid(root)
#     frame.pack(fill=tk.BOTH, expand=True)
#     files_array = files.search_files_from_user((2,))
#     #
#
#     ImageCard(frame).add_button(files_array[0]).add_file_name(files_array[0][2]).grid()
#     ImageCard(frame).add_button(files_array[1]).add_file_name(files_array[1][2]).grid()
#     ImageCard(frame).add_button(files_array[2]).add_file_name(files_array[2][2]).grid()
#     ImageCard(frame).add_button(files_array[3]).add_file_name(files_array[3][2]).grid()
#     print(files_array[3][2])
#
#     root.mainloop()


# example of using autogrid main
#if __name__ == '__main__':
#    main()
