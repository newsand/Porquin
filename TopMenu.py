#! /usr/bin/env python3
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import MainWindow as MW
from io import BytesIO
from struct import pack
from Crypto import Random
from Crypto.Cipher import Blowfish



from dbase import *
from FileBase import *
db = Database()
db.createTable()

files = Filebase()
files.createTable()


class TopMenu(tk.Menu):

    def __init__(self, master):
        tk.Menu.__init__(self, master, tearoff=False)
        self.controller = master
        
        vault = tk.Menu(self, tearoff=0)
        vault.add_command(label="Save file to vault", command=save_to_vault)
        vault.add_separator()
        vault.add_command(label="Close Session", command=lambda: self.master.switch_frame(MW.StartPage))
        vault.add_command(label="Exit", command=self.master.quit)
        self.add_cascade(label="Vault", menu=vault)

        edit = tk.Menu(self, tearoff=0)
        edit.add_command(label="Undo")
        edit.add_separator()
        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Paste")
        edit.add_command(label="Delete")
        edit.add_command(label="Select All")
        self.add_cascade(label="Edit", menu=edit)

        help_menu = Menu(self, tearoff=0)
        help_menu.add_command(label="About",command=about)
        self.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=self)


def save_file(file: bytes, filename: str):
    tosave = BytesIO(file).read()
    data = (2, filename, tosave)
    files.insertFile(data)

def save_to_vault():
    file = filedialog.askopenfilename(title="open")
    rfile = open(file, 'rb')
    tocrip = rfile.read()
    rfile.close()
    keyz = 'senhasatanica'.encode("utf-8")
    print(type(keyz))
    cripted_file = encrypt(keyz, tocrip)
    save_file(cripted_file, file.split('/')[-1])

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

def about():
    aboutmsg ='This is the Porquin File Vault\
              \n\nVersion: 0.1a\
              \n\nProposed and developed by Filipe Caporali\
              \n\nPorquin is made for safely stashing your files that you want to keep private!\
              \n\nThis is a free and open source version of this software made for useful and studying purposes.\
              \n\nAnyone can fork this project at will.'
    tk.messagebox.showinfo(title="About Porquin", message=aboutmsg)