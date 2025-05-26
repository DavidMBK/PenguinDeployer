import os
import re
import subprocess
from Module import Module


class PackagesLogic(Module):
    def __init__(self,nconfigfolder):
        super().__init__(nconfigfolder)

        self.to_install: list[str] = []
        self.to_uninstall: list[str] = []

        self.is_multi_import = True

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
        if not os.path.isabs(filename):
            filename = os.path.join(self.configfolder, filename)

        with open(filename, 'w') as confexp:
            for pack in self.to_install:
                confexp.write("\n" + pack + ":" + "install")
            for pack in self.to_uninstall:
                confexp.write("\n" + pack + ":" + "uninstall")

    def conf_import(self, filename):
        if not os.path.isabs(filename):
            filename = os.path.join(self.configfolder, filename)

        try:
            with open(filename) as conf:
                for line_num, line in enumerate(conf, start=1):
                    line = line.strip()
                    if not line:
                        continue  # salta righe vuote
                    if ':' not in line:
                        print(f"Riga {line_num} ignorata: '{line}' non contiene ':'")
                        continue
                    name, action = map(str.strip, line.split(":", 1))
                    if action == "install":
                        if name not in self.to_install:
                            self.to_install.append(name)
                    elif action == "uninstall":
                        if name not in self.to_uninstall:
                            self.to_uninstall.append(name)
                    else:
                        print(f"Riga {line_num} errore: azione non valida '{action}'")
        except FileNotFoundError:
            print(f"File non trovato: {filename}")
        except Exception as e:
            print(f"Errore durante l'importazione: {e}")


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

'''
if __name__ == "__main__":
    p = Packages(src/configs/packages)
    
    #testing import
    p.conf_import("testconfig.config")
    
    #testing export
    p.conf_export("testconfigexp.config")
    
    #testing configuration (install/uninstall)
    p.configure()
'''
