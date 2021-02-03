# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
# from t3 import ScrollableFrame, ImageCard
from struct import pack
from Crypto import Random
from Crypto.Cipher import Blowfish
from Configleton import Configleton
from TopMenu import TopMenu
from interface import BootstrapGrid

try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import filedialog
from io import BytesIO
import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage



from User import *
from FileBase import *

db = User()
db.createTable()

files = Filebase()
files.createTable()

BGC = "#123456"


class AppViewPage(tk.Frame):

    def __init__(self, master):
        # configure frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BGC)
        self.master.resizable(1, 1)
        self.master.minsize(height=300, width=350)
        self.menubar = TopMenu(self.master)
        self.menubar.vault.add_command(label="Save file to vault", command=self.save)
        self.menubar.vault.add_command(label="Delete", command=self.delete)
        # headers
        tk.Label(self, text="PorkinVault", font=('Helvetica', 18, "bold"), bg=BGC, fg="white").pack(side="top", fill="x", pady=5)
        self.frame = BootstrapGrid.ScrollableFrame(self)
        self.frame = self.restore()

    def save(self):
        self.menubar.save_to_vault()
        self.restore()

    def delete(self):
        self.menubar.delete(self.frame.selected_cards)
        self.restore()

    def restore(self):
        self.frame.destroy()
        self.frame = BootstrapGrid.ScrollableFrame(self)
        files_array = files.search_files_from_user(Configleton.shared_instance()._USER)

        for iteration, x in enumerate(files_array):
            print(x[0])
            y = (x[0], x[1], x[2], decrypt_image(x[3]))
            BootstrapGrid.ImageCard(self.frame.scrollable_frame).add_button(y).add_file_name(x[2]).add_file_id(x[0]).grid()
            self.frame.pack(side="left", fill=tk.BOTH, expand=True)
        return self.frame


def stream_to_image(stream) -> Image:
    stream = BytesIO(stream)
    im = Image.open(stream).convert("RGBA")
    stream.close()
    return im


def generate_thumbnail(xablau) -> PhotoImage:
    im = stream_to_image(xablau)
    im.thumbnail((128, 128), Image.ANTIALIAS)
    icon = PIL.ImageTk.PhotoImage(im)
    return icon


def save_image(file_path: str):
    image = PIL.Image.open("luigi.jpg")
    tosave = BytesIO()
    image.save(tosave, format='PNG')
    tosave = tosave.getvalue()
    data = (2, image.filename, tosave)
    files.insertData(data)


def save_file(file: bytes, filename: str):
    tosave = BytesIO(file).read()
    data = (2, filename, tosave)
    #    print(data)
    files.insertFile(data)


def onOpen():
    file = filedialog.askopenfilename(title="open")
    rfile = open(file, 'rb')
    tocrip = rfile.read()
    rfile.close()
    keyz = 'senhasatanica'.encode("utf-8")
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


def decrypt(key, file):
    bs = Blowfish.block_size

    ciphertext = file
    iv = ciphertext[:bs]
    ciphertext = ciphertext[bs:]

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    msg = cipher.decrypt(ciphertext)

    last_byte = msg[-1]
    msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]

    # return msg.decode('utf-8')
    return msg


def decrypt_image(file):
    keyz = Configleton.shared_instance().get_cryptokey().encode("utf-8")
    cripted_file = decrypt(keyz, file)
    stream = BytesIO(cripted_file).read()
    # image = Image.open(stream).convert("RGBA")
    return stream
