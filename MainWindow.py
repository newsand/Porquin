# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
from io import BytesIO
from math import floor
import random

import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage

try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, FLAT, BOTH, Menu
from dbase import *
from FileBase import *

db = Database()
db.createTable()

files = Filebase()
files.createTable()

BGC = "#123456"


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('porkit')
        self.resizable(0, 0)
        self.config(bg=BGC)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BGC)
        tk.Label(self, text="FileVault", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Login", command=lambda: master.switch_frame(LoginPage)).pack()
        tk.Button(self, text="Register", command=lambda: master.switch_frame(RegisterPage)).pack()


class LoginPage(tk.Frame):
    def login(self):
        self.master.switch_frame(AppViewPage).pack()

    def __init__(self, master):
        self.usernameS = tk.StringVar()
        self.passwordS = tk.StringVar()

        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BGC)
        tk.Label(self, text="Login", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self, textvariable=self.usernameS)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*", textvariable=self.passwordS)
        pass_entry.pack()
        login_button = Button(self, text="Login", command=self.validate)
        login_button.pack()

    def validate(self):
        username = self.usernameS.get()
        password = self.passwordS.get()
        data = (username,)
        print(data)
        inputData = (username, password,)
        print(inputData)
        try:
            if (db.validateData(data, inputData)):
                messagebox.showinfo("Successful", "Login Was Successful")
                self.login()
            else:
                messagebox.showerror("Error", "Wrong Credentials")
        except IndexError:
            messagebox.showerror("Error", "Wrong Credentials")


class RegisterPage(tk.Frame):
    def register(self):
        print('register')

    def __init__(self, master):
        self.usernameS = tk.StringVar()
        self.passwordS = tk.StringVar()
        self.ConfpasswordS = tk.StringVar()

        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BGC)
        tk.Label(self, text="Register", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self, textvariable=self.usernameS)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*", textvariable=self.passwordS)
        pass_entry.pack()
        conf_label = Label(self, text="Confirmação", bg=BGC, fg="white")
        conf_label.pack()
        conf_entry = Entry(self, show="*", textvariable=self.ConfpasswordS)
        conf_entry.pack()
        register_button = Button(self, text="Register", command=self.add)
        register_button.pack()

        self.salt = bcrypt.gensalt()

    def add(self):
        username = self.usernameS.get()
        password = self.passwordS.get()
        confpassword = self.ConfpasswordS.get()
        self.hashed = bcrypt.hashpw(password.encode(), self.salt)
        data = (username,)
        print(data)
        print(password)
        print(confpassword)

        result = db.searchData(data)
        print(result)
        if result != 0:
            data = (username, self.hashed)
            db.insertData(data)
            messagebox.showinfo("Successful", "Username Was Added")
        else:
            messagebox.showwarning("Warning", "Username already Exists")


class AppViewPage(tk.Frame):

    def men_bar(self):
        menubar = Menu(self)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")

        file.add_separator()
        file.add_command(label="Close Session", command=lambda: self.master.switch_frame(StartPage))
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

        filesarray = files.search_files_from_user((2,))
        for iteration, x in enumerate(filesarray):
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


if __name__ == "__main__":
    app = MainWindow()

    app.mainloop()
