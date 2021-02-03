from interface.MainWindow import MainWindow
from Configleton import Configleton
from User import *
from FileBase import *


files = Filebase()
files.createTable()
if __name__ == "__main__":
    Configleton.shared_instance().set_cryptkey("senhasatanica")
    #print(Configleton.shared_instance().get_cryptokey())

    db = User()
    db.createTable()
    files = Filebase()
    files.createTable()
    db.finish()
    files.finish()

    app = MainWindow()
    app.mainloop()

