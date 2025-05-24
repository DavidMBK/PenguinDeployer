from packages import Packages
from services import Services
from logger import Login

# Parte GUI
from tkinter import Tk
from main_ui import MainUI


class Main:

    pack: Packages
    service: Services

    def main(self):

        #performa il log-in
        log = Login()
        log.adminlogin()

        if not log.admin:
            exit()

        #inizializza moduli
        self.pack = Packages("src/configs/packages")
        self.service = Services("src/configs/services")

        #codice temporaneo
        print("Configura il sistema? Y/N")
        ans = input()
        if ans == "Y":
            self.runconfig()
        else:
            exit()

    def runconfig(self):

        self.pack.configure()
        self.service.configure()

        print("Configurazione completata")


if __name__=="__main__":
    # m = Main()
    # m.main()

    # Questo è la configurazione con best practise dell'UI

    root = Tk()
    app = MainUI(root)
    root.mainloop()