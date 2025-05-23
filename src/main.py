from packages import Packages
from services import Services

class Main:

    pack: Packages
    service: Services

    def main(self):

        #inizializza moduli
        self.pack = Packages()
        self.service = Services()

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
    m = Main()
    m.main()