# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
import time

from interface import StartPage

try:
    import Tkinter as tk
except:
    import tkinter as tk
from Configleton import Configleton
from User import User
from interface.AppViewPage import AppViewPage
from tkinter import Label, messagebox, Entry, Button
BGC = Configleton.shared_instance().get_required_config_var("BGC")

class LoginPage(tk.Frame):
    def login(self):
        self.master.switch_frame(AppViewPage).pack()

    def __init__(self, master):
        self.usernameS = tk.StringVar()
        self.passwordS = tk.StringVar()
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BGC)
        tk.Label(self, text="Login", bg=BGC, fg='white',font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage.StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self, textvariable=self.usernameS)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*", textvariable=self.passwordS)
        pass_entry.pack()
        login_button = Button(self, text="Login", command=self.validate)
        login_button.pack(fill='x',pady=5)
        #print(Configleton.shared_instance().get_cryptokey())

    def validate(self):
        username = self.usernameS.get()
        password = self.passwordS.get()
        data = (username,)
        inputData = (username, password,)

        user_table = User()
        try:
            if user_table.validateData(data, inputData):
                Configleton.shared_instance()._USER = user_table.get_id(data)
                messagebox.showinfo("Successful", "Login Was Successful")
                self.login()
            else:
                messagebox.showerror("Error", "Wrong Credentials")
                time.sleep(5)
        except IndexError:
            messagebox.showerror("Error", "Wrong Credentials")
            time.sleep(1)
        user_table.finish()