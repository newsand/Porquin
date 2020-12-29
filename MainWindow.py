# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import Label, Button, Entry, messagebox
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
        tk.Frame.configure(self, bg= BGC)
        tk.Label(self, text="Login", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self,textvariable=self.usernameS)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*",textvariable=self.passwordS)
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
        tk.Frame.configure(self, bg= BGC)
        tk.Label(self, text="Register", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self,textvariable=self.usernameS)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*",textvariable=self.passwordS)
        pass_entry.pack()
        conf_label = Label(self, text="Confirmação", bg=BGC, fg="white")
        conf_label.pack()
        conf_entry = Entry(self, show="*",textvariable=self.ConfpasswordS)
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
    def quit(self):
        print('quit')

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='red')
        tk.Label(self, text="Inside!", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        hello_label = Label(self, text="HELOOO MODAFOKA", bg=BGC, fg="white")
        hello_label.pack()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
