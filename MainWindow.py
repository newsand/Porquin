# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
from Configleton import Configleton
try:
    import Tkinter as tk
except:
    import tkinter as tk
from RegisterPage import RegisterPage
from LoginPage import LoginPage
BGC = Configleton.shared_instance().get_required_config_var("BGC")


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Porquin')
        self.resizable(0, 0)
        self.config(bg=BGC)
        self._frame = None
        self.switch_frame(StartPage)

    # navigation system
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fil=tk.BOTH)


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BGC)
        tk.Label(self, text="FileVault", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Login", command=lambda: master.switch_frame(LoginPage)).pack()
        tk.Button(self, text="Register", command=lambda: master.switch_frame(RegisterPage)).pack()