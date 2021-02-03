#! /usr/bin/env python3
import tkinter as tk
from tkinter import *
from tkinter import filedialog

from Configleton import Configleton
from interface import MainWindow as Mw
from io import BytesIO
from struct import pack
from Crypto import Random
from Crypto.Cipher import Blowfish
from FileBase import *


class TopMenu(tk.Menu):

    def __init__(self, master):
        tk.Menu.__init__(self, master, tearoff=False)
        self.controller = master
        self.vault = tk.Menu(self, tearoff=0)
        self.vault.add_command(label="Close Session", command=lambda: self.master.switch_frame(Mw.StartPage))
        self.vault.add_command(label="Exit", command=self.master.quit)
        self.vault.add_separator()
        self.add_cascade(label="Vault", menu=self.vault)

        self.edit = tk.Menu(self, tearoff=0)
        self.edit.add_command(label="Undo")
        self.edit.add_separator()
        self.edit.add_command(label="Cut")
        self.edit.add_command(label="Copy")
        self.edit.add_command(label="Paste")
        self.edit.add_command(label="Delete")
        self.edit.add_command(label="Select All")
        self.add_cascade(label="Edit", menu=self.edit)

        self.help_menu = Menu(self, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.add_cascade(label="Help", menu=self.help_menu)

        self.master.config(menu=self)

    def save_file(self, file: bytes, filename: str):
        tosave = BytesIO(file).read()
        data = (Configleton.shared_instance()._USER[0], filename, tosave)
        files = Filebase()
        files.insertFile(data)
        files.finish()

    def save_to_vault(self):
        file = filedialog.askopenfilename(title="open")
        print(file)
        rfile = open(file, 'rb')
        tocrip = rfile.read()
        rfile.close()
        keyz = Configleton.shared_instance().get_cryptokey().encode("utf-8")
        cripted_file = self.encrypt(keyz, tocrip)
        self.save_file(cripted_file, file.split('/')[-1])

    def delete(self, files: list):

        files = Filebase()
        files.delete_files(files)
        files.finish()

    def encrypt(self, key: bytes, file: bytes):
        bs = Blowfish.block_size
        iv = Random.new().read(bs)
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
        plaintext = file
        plen = bs - divmod(len(plaintext), bs)[1]
        padding = [plen] * plen
        padding = pack('b' * plen, *padding)
        text = cipher.IV + cipher.encrypt(plaintext + padding)
        return text

    def about(self):
        aboutmsg = 'This is the Porquin File Vault\
                  \n\nVersion: 0.1a\
                  \n\nProposed and developed by Filipe Caporali\
                  \n\nPorquin is made for safely stashing your files that you want to keep private!\
                  \n\nThis is a free and open source version of this software made for useful and studying purposes.\
                  \n\nAnyone can fork this project at will.'
        tk.messagebox.showinfo(title="About Porquin", message=aboutmsg)
