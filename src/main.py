from packages import PackagesLogic
from services import Services
from logger import Login

# Parte GUI
from tkinter import Tk
from Main_UI import MainUI


class Main:

    pack: PackagesLogic
    service: Services

    def main(self):

        #performa il log-in
        log = Login()
        log.adminlogin()

        if not log.admin:
            exit()

        #inizializza moduli
        self.pack = PackagesLogic("src/configs/packages")
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
    nconfigfolder = "src/configs/packages"

    root = Tk()
    app = MainUI(root, nconfigfolder)
    root.mainloop()