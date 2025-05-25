from packages import Packages
from services import Services
from logger import Login

# Parte GUI
from ttkthemes import ThemedTk
from Main_UI import MainUI


class Main:

    pack: Packages
    service: Services

    def main(self):

        #inizializza l'UI
        root = ThemedTk()
        #style = ttk.Style(root)
        #style.theme_use("equilux")
        app = MainUI(root)

        #inizializza moduli
        self.pack = Packages("src/configs/packages")
        self.service = Services("src/configs/services")

        root.mainloop()

    def runconfig(self):

        self.pack.configure()
        self.service.configure()

        print("Configurazione completata")


if __name__=="__main__":
    m = Main()
    m.main()
