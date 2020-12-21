try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import Label, Button, Entry

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
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg= BGC)
        tk.Label(self, text="Login", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*")
        pass_entry.pack()
        login_button = Button(self, text="Login", command=self.login)
        login_button.pack()


class RegisterPage(tk.Frame):
    def register(self):
        print('register')

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg= BGC)
        tk.Label(self, text="Register", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*")
        pass_entry.pack()
        conf_label = Label(self, text="Confirmação", bg=BGC, fg="white")
        conf_label.pack()
        conf_entry = Entry(self, show="*")
        conf_entry.pack()
        register_button = Button(self, text="Register", command=self.register)
        register_button.pack()


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
