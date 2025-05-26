import tkinter as tk
from Logger_UI import LoginFrame
from Mainwindow_UI import Mainwindow

class MainUI:

    def __init__(self, main):

        self.main = main

        # Costruzione basica del frame, [Devo farla dinamica?]
        self.root = tk.Tk()
        self.root.title("PenguinDeployer")

        # Istanzio i frame, passando root, controller e modulo se necessario (self)
        loginf = LoginFrame(self.root, self, self.main.logger)
        mainwindowf = Mainwindow(self.root, self, self.main)  # passa in input l'array di frame

        # Lo salvo nel dizionario con chiave il nome della classe
        self.frames = {
            mainwindowf.__class__.__name__: mainwindowf,
            loginf.__class__.__name__: loginf,
        }

        # Posiziono i frame dentro root, occupa tutta la finestra
        for FrameClass in self.frames.keys():
            self.frames[FrameClass].place(relwidth=1, relheight=1)

        # self.show_frame("LoginFrame")
        self.show_frame("Mainwindow")

        self.root.mainloop()

    # metodo per passaggio frame    
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        self.modular(name)

    def center_window(self, width, height):
        user_screen_width = self.root.winfo_screenwidth()
        user_screen_height = self.root.winfo_screenheight()
        x = (user_screen_width - width) // 2  # Interi non float accettati
        y = (user_screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def modular(self, name):
        if name == "LoginFrame":
            self.center_window(925, 500)
            self.root.resizable(False, False)
        elif name == "Mainwindow":
            self.center_window(1200, 800)
            self.root.resizable(True, True)
