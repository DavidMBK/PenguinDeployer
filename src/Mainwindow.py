import tkinter as tk

class Mainwindow():

    def __init__(self):

        #probabilmente questo va' messo nel main e passato alle classi della GUI
        self.tkroot = tk.Tk()
        self.tkroot.title = "PenguinDeploy"
        self.tkroot.geometry("800x500")

        #rimuovi i border dai frame dopo

        #sidebar
        self.sidebar = tk.Frame(self.tkroot,pady=4,padx=4)
        self.sidebar.pack(fill=tk.BOTH,side=tk.LEFT)

        #frame principale
        self.main_frame = tk.Frame(self.tkroot,borderwidth="3",relief="ridge",width=400,height=30)
        self.main_frame.pack(expand=True,fill=tk.BOTH,side=tk.RIGHT)

        #bottoni per i moduli
        self.modulebutton = tk.Button(self.sidebar, text='Module1', command=self.SubmitForm, width="30", height="3")
        self.modulebutton.pack(pady=3)

        self.modulebutton2 = tk.Button(self.sidebar, text='Module2', command=self.SubmitForm, width="30", height="3")
        self.modulebutton2.pack(pady=3)

        #bottone per applicare le configurazioni
        self.apply = tk.Button(self.sidebar,text="Apply Configurations",command=self.SubmitForm,width="30",height="3")
        self.apply.pack(side=tk.BOTTOM)

        self.tkroot.mainloop()


    def SubmitForm(self):
        #test per i bottoni, da rimuovere
        print("button pressed")

mw = Mainwindow()