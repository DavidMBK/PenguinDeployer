import tkinter as tk
from Logger_UI import LoginFrame
from Mainwindow_UI import Mainwindow

class MainUI:
    def __init__(self, root):
        # Costruzione basica del frame, [Devo farla dinamica?]
        self.root = root
        self.root.title("PenguinDeployer")

        self.frames = {}  # Creo un dizionario vuoto che conterrà i vari "frame" (pagine)

        for FrameClass in (LoginFrame, Mainwindow):
            page = FrameClass(self.root, self)  # Istanzio un frame, passando root e controller (self)
            self.frames[FrameClass.__name__] = page  # Lo salvo nel dizionario con chiave il nome della classe
            page.place(relwidth=1, relheight=1)  # Posiziono il frame dentro root, occupa tutta la finestra


        #self.show_frame("LoginFrame")
        self.show_frame("Mainwindow")
        
    # metodo per passaggio frame    
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        self.modular(name)

    def center_window(self, width, height):
        user_screen_width = self.root.winfo_screenwidth()
        user_screen_height = self.root.winfo_screenheight()
        x = (user_screen_width - width) // 2 # Interi non float accettati
        y = (user_screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def modular(self, name):
        if name == "LoginFrame":
            self.center_window(925,500)
            self.root.resizable(False, False)
        elif name == "Mainwindow":
            self.center_window(1200,800)
            self.root.resizable(True, True)


