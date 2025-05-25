import tkinter as tk
from tkinter import messagebox

class Mainwindow(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #rimuovi i border dai frame dopo

        #sidebar
        self.sidebar = tk.Frame(self, pady=4, padx=4)
        self.sidebar.pack(fill=tk.BOTH, side=tk.LEFT)

        #frame principale
        self.main_frame = tk.Frame(self, borderwidth="3", relief="ridge", width=400, height=30)
        self.main_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

        #bottoni per i moduli
        self.modulebutton = tk.Button(self.sidebar, text='Installazione Software', command=self.SubmitForm, width="30", height="3")
        self.modulebutton.pack(pady=3)

        self.modulebutton2 = tk.Button(self.sidebar, text='Gestione Servizi', command=self.SubmitForm, width="30", height="3")
        self.modulebutton2.pack(pady=3)

        self.modulebutton3 = tk.Button(self.sidebar, text='Personalizzazione Ambiente', command=self.SubmitForm, width="30", height="3")
        self.modulebutton3.pack(pady=3)

        self.modulebutton4 = tk.Button(self.sidebar, text='Configurazione Veloce', command=self.SubmitForm, width="30", height="3")
        self.modulebutton4.pack(pady=3)

        self.modulebutton5 = tk.Button(self.sidebar, text='Revert', command=self.SubmitForm, width="30", height="3")
        self.modulebutton5.pack(pady=3)

        #bottone per applicare le configurazioni
        self.apply = tk.Button(self.sidebar,text="Apply Configurations",command=self.Applychanges,width="30",height="3")
        self.apply.pack(side=tk.BOTTOM)


    def SubmitForm(self):
        #test per i bottoni, da rimuovere
        print("button pressed")

    # Semplice modal, non c'è bisogno di creare un frame a parte per questo.
    def Applychanges(self):
        response = messagebox.askquestion("Confirm Changes", "Do you want to apply the changes?")
        if response == "yes":
            print("Success")
        elif response == "no":
            print("Error")

