# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
#from t3 import ScrollableFrame, ImageCard

from Crypto import Random
from Crypto.Cipher import Blowfish
from struct import pack
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import Label, FLAT, Menu, BOTH, filedialog
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
        file.add_command(label="Save file to vault", command=onOpen)
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
        self.master.minsize(height=300, width=350)

        self.men_bar()

        # headers
        tk.Label(self, text="PorkinVault", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        hello_label = Label(self, text="HELOOO MODAFOKA", bg=BGC, fg="white")
        hello_label.pack()

        frame = BootstrapGrid.ScrollableFrame(self)
        files_array = files.search_files_from_user((2,))

        for iteration, x in enumerate(files_array):
            print(type(x))
            y=(x[0],x[1],x[2],decrypt_image(x[3]))
            #print (x)
            BootstrapGrid.ImageCard(frame.scrollable_frame).add_button(y).add_file_name(x[2]).grid()
            print(iteration)

        frame.pack(side="left", fill=tk.BOTH, expand=True)



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



def save_image(file_path:str):
    image =PIL.Image.open("luigi.jpg")
    tosave = BytesIO()
    image.save(tosave, format='PNG')
    tosave = tosave.getvalue()
    data = (2,image.filename, tosave)
    files.insertData(data)

def save_file(file:bytes,filename:str):
    tosave = BytesIO(file).read()
    data = (2,filename, tosave)
#    print(data)

    files.insertFile(data)

def onOpen():
    file = filedialog.askopenfilename(title="open")
    rfile = open(file, 'rb')
    # print(rfile)
    tocrip = rfile.read()
    # print(tocrip)
    print(type(tocrip))
    rfile.close()

    keyz = 'senhasatanica'.encode("utf-8")
    print(type(keyz))
    cripted_file = encrypt(keyz, tocrip)
    save_file(cripted_file,file.split('/')[-1])


def encrypt(key: bytes, file: bytes):
    bs = Blowfish.block_size
    iv = Random.new().read(bs)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plaintext = file
    plen = bs - divmod(len(plaintext), bs)[1]
    padding = [plen] * plen
    padding = pack('b' * plen, *padding)
    text = cipher.IV + cipher.encrypt(plaintext + padding)
    return (text)

def decrypt(key, file):
    bs = Blowfish.block_size

    ciphertext = file
    iv = ciphertext[:bs]
    ciphertext = ciphertext[bs:]

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    msg = cipher.decrypt(ciphertext)

    last_byte = msg[-1]
    msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]

    #return msg.decode('utf-8')
    return msg

def decrypt_image(file):
    keyz = 'senhasatanica'.encode("utf-8")
    cripted_file = decrypt(keyz, file)
    stream = BytesIO(cripted_file).read()
    #image = Image.open(stream).convert("RGBA")
    return stream
