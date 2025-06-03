from functools import partial
import tkinter as tk
from tkinter import messagebox
from Packages_UI import PackagesUI
from Services_UI import ServicesUI
from Environment_UI import EnvironmentUI
from Quickconfig_UI import QuickConfigUI


# Importa qui altri frame/moduli quando li hai, es:
# from ServiceManagement_UI import ServiceManagementUI
# from Personalization_UI import PersonalizationUI
# ecc.

class Mainwindow(tk.Frame):
    def __init__(self, parent, controller, main, env_manager=None, service_manager = None, pack_manager=None):
        super().__init__(parent)
        # Inzializzazione 
        self.controller = controller
        self.main = main
        self.env_manager = env_manager
        self.service_manager = service_manager
        self.pack_manager = pack_manager

        self.sidebar = tk.Frame(self, pady=4, padx=4)
        self.sidebar.pack(fill=tk.BOTH, side=tk.LEFT)

        # Area principale a destra dove caricare i frame
        self.main_frame = tk.Frame(self, borderwidth=3, relief="ridge")
        self.main_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

        self.moduleframes = [
            PackagesUI(self.main_frame, self, self.main.pack, self.service_manager),
            ServicesUI(self.main_frame, self, self.main.service, self.pack_manager),
            EnvironmentUI(self.main_frame, self, self.main.environment.configfolder, self.env_manager),
            QuickConfigUI(self.main_frame, self, self.main.quick) 

        ]  # aggiungere gli altri man mano

        # Riferimento al frame corrente mostrato
        self.current_frame = None

        # Pulsanti sidebar con callback che caricano i frame
        self.modulebuttons = []
        for frame in self.moduleframes:

            text = ""
            fname = frame.__class__.__name__
            match fname:
                case "PackagesUI":
                    text = "Installazione Software"
                case "ServicesUI":
                    text = "Installazione Servizi"
                case "EnvironmentUI":
                    text = "Configurazione Ambiente"
                case "QuickConfigUI":
                    text = "Configurazione Veloce"
                #aggiungi altri

            modulebutton = tk.Button(self.sidebar, text=text,
                                     command=partial(self.show_frame,fname), width=30, height=3)
            modulebutton.pack(pady=3)
            self.modulebuttons.append(modulebutton)

        # Bottone per applicare le configurazioni
        self.apply = tk.Button(self.sidebar, text="Apply Configurations",
                               command=self.Applychanges, width=30, height=3)
        self.apply.pack(side=tk.BOTTOM, pady=10)

        # Puoi caricare un frame di default, ad esempio PackagesUI
        self.show_frame("PackagesUI")

    def show_frame(self, frame_name):
        # Distruggi frame corrente se esiste
        if self.current_frame:
            self.current_frame.pack_forget()

        for frame in self.moduleframes:
            if frame.__class__.__name__ == frame_name:
                self.current_frame = frame
                if frame_name == "EnvironmentUI" or frame_name == "PackagesUI" or frame_name == "ServicesUI":
                    self.current_frame.refresh_from_manager()
                    
                self.current_frame.pack(fill=tk.BOTH, expand=True)
                return

        self.current_frame = self.placeholder_frame(f"Frame '{frame_name}' non trovato")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def Applychanges(self): # Semplice Modal
        response = messagebox.askquestion("Confirm Changes", "Do you want to apply the changes?")
        if response == "yes":
            self.main.runconfig()
        elif response == "no":
            return

    def placeholder_frame(self, message):
        # Frame semplice per placeholder se il frame non è implementato
        frame = tk.Frame(self.main_frame)
        label = tk.Label(frame, text=message, fg="red", font=("Arial", 14))
        label.pack(expand=True)
        return frame
