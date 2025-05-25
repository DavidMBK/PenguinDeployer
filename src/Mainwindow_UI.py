import tkinter as tk
from tkinter import messagebox
from Package_installer_UI import PackagesUI
# Importa qui altri frame/moduli quando li hai, es:
# from ServiceManagement_UI import ServiceManagementUI
# from Personalization_UI import PersonalizationUI
# ecc.

class Mainwindow(tk.Frame):
    def __init__(self, parent, controller, nconfigfolder):
        super().__init__(parent)
        self.controller = controller
        self.nconfigfolder = nconfigfolder

        # Sidebar a sinistra
        self.sidebar = tk.Frame(self, pady=4, padx=4)
        self.sidebar.pack(fill=tk.BOTH, side=tk.LEFT)

        # Area principale a destra dove caricare i frame
        self.main_frame = tk.Frame(self, borderwidth=3, relief="ridge")
        self.main_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

        # Riferimento al frame corrente mostrato
        self.current_frame = None

        # Pulsanti sidebar con callback che carica i frame
        self.modulebutton = tk.Button(self.sidebar, text='Installazione Software',command=lambda: self.show_frame("PackagesUI"), width=30, height=3)
        self.modulebutton.pack(pady=3)

        self.modulebutton2 = tk.Button(self.sidebar, text='Gestione Servizi',
                                       command=lambda: self.show_frame("ServiceManagementUI"),
                                       width=30, height=3)
        self.modulebutton2.pack(pady=3)

        self.modulebutton3 = tk.Button(self.sidebar, text='Personalizzazione Ambiente',
                                       command=lambda: self.show_frame("PersonalizationUI"),
                                       width=30, height=3)
        self.modulebutton3.pack(pady=3)

        self.modulebutton4 = tk.Button(self.sidebar, text='Configurazione Veloce',
                                       command=lambda: self.show_frame("QuickConfigUI"),
                                       width=30, height=3)
        self.modulebutton4.pack(pady=3)

        self.modulebutton5 = tk.Button(self.sidebar, text='Revert',
                                       command=lambda: self.show_frame("RevertUI"),
                                       width=30, height=3)
        self.modulebutton5.pack(pady=3)

        # Bottone per applicare le configurazioni
        self.apply = tk.Button(self.sidebar, text="Apply Configurations",
                               command=self.Applychanges, width=30, height=3)
        self.apply.pack(side=tk.BOTTOM, pady=10)

        # Puoi caricare un frame di default, ad esempio PackagesUI
        self.show_frame("PackagesUI")

    def show_frame(self, frame_name):
        # Distruggi frame corrente se esiste
        if self.current_frame:
            self.current_frame.destroy()

        # Crea il frame corrispondente
        if frame_name == "PackagesUI":
            self.current_frame = PackagesUI(self.main_frame, self.controller, self.nconfigfolder)
        elif frame_name == "ServiceManagementUI":
            # self.current_frame = ServiceManagementUI(self.main_frame, self.controller, self.nconfigfolder)
            self.current_frame = self.placeholder_frame("Gestione Servizi non implementato")
        elif frame_name == "PersonalizationUI":
            # self.current_frame = PersonalizationUI(self.main_frame, self.controller, self.nconfigfolder)
            self.current_frame = self.placeholder_frame("Personalizzazione Ambiente non implementato")
        elif frame_name == "QuickConfigUI":
            # self.current_frame = QuickConfigUI(self.main_frame, self.controller, self.nconfigfolder)
            self.current_frame = self.placeholder_frame("Configurazione Veloce non implementata")
        elif frame_name == "RevertUI":
            # self.current_frame = RevertUI(self.main_frame, self.controller, self.nconfigfolder)
            self.current_frame = self.placeholder_frame("Revert non implementato")
        else:
            self.current_frame = self.placeholder_frame(f"Frame '{frame_name}' non trovato")

        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def Applychanges(self):
        response = messagebox.askquestion("Confirm Changes", "Do you want to apply the changes?")
        if response == "yes":
            print("Success")
        elif response == "no":
            print("Error")

    def placeholder_frame(self, message):
        # Frame semplice per placeholder se il frame non è implementato
        frame = tk.Frame(self.main_frame)
        label = tk.Label(frame, text=message, fg="red", font=("Arial", 14))
        label.pack(expand=True)
        return frame
