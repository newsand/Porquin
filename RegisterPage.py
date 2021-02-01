try:
    import Tkinter as tk
except:
    import tkinter as tk

from tkinter import Label, messagebox, Entry, Button
from MainWindow import *
from User import *
import StartPage
BGC = "#123456"



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
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage.StartPage)).pack()
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
        user_table = User()
        result = user_table.searchData(data)
        print(result)
        if result != 0:
            data = (username, self.hashed)
            user_table.insertData(data)
            messagebox.showinfo("Successful", "Username Was Added")
        else:
            messagebox.showwarning("Warning", "Username already Exists")
        user_table.finish()