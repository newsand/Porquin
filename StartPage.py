import LoginPage
import RegisterPage
from Configleton import Configleton
try:
    import Tkinter as tk
except:
    import tkinter as tk
BGC = Configleton.shared_instance().get_required_config_var("BGC")


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BGC)
        tk.Label(self, text="Porquin", font=('Helvetica', 18, "bold"),bg=BGC,fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Login", command=lambda: master.switch_frame(LoginPage.LoginPage)).pack( fill="x")
        tk.Button(self, text="Register", command=lambda: master.switch_frame(RegisterPage.RegisterPage)).pack( fill="x")