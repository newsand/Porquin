from tkinter import *

class Application:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack(side=RIGHT)
        self.msg = Label(self.widget1, text="Primeiro widget")
        self.msg["font"] = ("Verdana", "10", "italic", "bold")
        self.msg.pack()
        self.sair = Button(self.widget1)
        self.sair["text"] = "Clique aqui"
        self.sair["font"] = ("Verdana", "10")
        self.sair["width"] = 10
        self.sair.bind("<Button-1>", self.mudarTexto)
        self.sair.pack()
        pass

    def mudarTexto(self, event):
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"
        else:
            self.msg["text"] = "Primeiro widget"
root = Tk()
Application(root)
root.mainloop()