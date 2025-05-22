import re
import subprocess
from module import Module


class Packages(Module):
    to_install: list[str]
    to_uninstall: list[str]

    def install_packages(self):
        #esegui lo script per installare i pacchetti
        run = ["./src/scripts/install.sh"] + self.to_install
        subprocess.call(run)

    def unistall_packages(self):
        # esegui lo script per disnstallare i pacchetti
        run = ["./src/scripts/uninstall.sh"] + self.to_uninstall
        subprocess.call(run)

    def sys_read(self):
        #aggiungere
        pass

    def conf_export(self, filename):

        confexp = open(filename, 'a')

        for pack in self.to_install:
            confexp.write("\n" + pack + ":" + "install")

        for pack in self.to_uninstall:
            confexp.write("\n" + pack + ":" + "uninstall")

    def conf_import(self, filename):

        conf = open(filename)
        packages = conf.read()
        psplit = re.split(':|\n', packages)

        i = 0
        while i < len(psplit) / 2:
            if psplit[i + 1] == "install":
                self.to_install.append(psplit[i])
            elif psplit[i + 1] == "uninstall":
                self.to_uninstall.append(psplit[i])
            else:
                print("Errore nel file di configurazione")
            i += 2

    def configure(self):

        self.install_packages()
        self.unistall_packages()



if __name__ == "__main__":
    p = Packages()
    
    #testing import
    p.conf_import("src/configs/packages/testconfig.config")
    
    #testing export
    p.conf_export("src/configs/packages/testconfigexp.config")
    
    #testing configuration (install/uninstall)
    p.configure()

