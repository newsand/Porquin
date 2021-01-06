# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/

try:
    import Tkinter as tk
except:
    import tkinter as tk

from RegisterPage import RegisterPage
from LoginPage import LoginPage



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



