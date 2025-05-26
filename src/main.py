from Packages import PackagesLogic
from Services import ServicesLogic
from Quickconfig import QuickConfig
from environment import EnvironmentLogic
from Logger import Login
from Main_UI import MainUI


class Main:

    def __init__(self):

        #inizilizza altre classi
        self.logger = Login()

        #inizializza i moduli
        self.pack = PackagesLogic("src/configs/packages")
        self.service = ServicesLogic("src/configs/services")
        self.environment = EnvironmentLogic("src/configs/environment")
        self.quick = QuickConfig([self.pack, self.service, self.environment])

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
