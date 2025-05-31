import os
import re
import subprocess
from Module import Module


class PackagesLogic(Module):
    def __init__(self, nconfigfolder):
        super().__init__(nconfigfolder)

        self.to_install: list[str] = []  # lista dei pacchetti da installare
        self.to_uninstall: list[str] = []  # lista dei pacchetti da disinstallare

        self.is_multi_import = True  # flag per segnare che la classe importa più di un file alla volta

    def install_packages(self):
        # esegui lo script per installare i pacchetti
        run = ["./src/scripts/install.sh"] + self.to_install
        subprocess.call(run)

    def unistall_packages(self):
        # esegui lo script per disnstallare i pacchetti
        run = ["./src/scripts/uninstall.sh"] + self.to_uninstall
        subprocess.call(run)

    def conf_export(self, filename):

        confexp = open(self.configfolder + "/" + filename, 'w')

        for pack in self.to_install:
            confexp.write("\n" + pack + ":" + "install")

        for pack in self.to_uninstall:
            confexp.write("\n" + pack + ":" + "uninstall")

    def conf_import(self, filename):

        conf = open(self.configfolder + "/" + filename)
        packages = conf.read()
        psplit = re.split(':|\n', packages)

        psplit = list(filter(None, psplit))

        i = 0
        while i < len(psplit):
            if psplit[i + 1] == "install":
                if psplit[i + 1] not in self.to_install:
                    self.to_install.append(psplit[i])
            elif psplit[i + 1] == "uninstall":
                if psplit[i + 1] not in self.to_uninstall:
                    self.to_uninstall.append(psplit[i])
            else:
                print("Errore nel file di configurazione")
            i += 2

    def conf_import_multiple(self, filenames):

        self.to_install = []
        self.to_uninstall = []

        for filename in filenames:
            self.conf_import(filename)


    def configure(self):

        self.install_packages()
        self.unistall_packages()

    def prova(self):
        print(f'installati: {self.to_install}')
        print(f'Disinstallati: {self.to_uninstall}')

    def find_package(self, query):
        comand = ["./src/scripts/search_pack.sh"] + [query]
        result = subprocess.run(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        matches = [line.split(" - ")[0] for line in result.stdout.strip().split("\n") if line]
        return matches
