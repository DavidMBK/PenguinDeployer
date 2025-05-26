from Packages import PackagesLogic
from Services import Services
from Logger import Login
from Main_UI import MainUI


class Main:

    def __init__(self):

        #inizilizza altre classi
        self.logger = Login()

        #inizializza i moduli
        self.pack = PackagesLogic("src/configs/packages")
        self.service = Services("src/configs/services")

        #inizialliza l'UI principale
        self.mainUI = MainUI(self)

    def main(self):
        pass

    def runconfig(self):

        self.pack.configure()
        self.service.configure()

        print("Configurazione completata")


if __name__=="__main__":
    m = Main()
    m.main()
