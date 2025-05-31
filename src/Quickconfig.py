import os
import shutil
import subprocess


class QuickConfig:

    selected_configs: dict

    def __init__(self, modules):

        self.modules = modules
        self.selected_configs = {}

        # inserisci i moduli in un dizionario, per poi associare ad ogni modulo
        # un file selezionato per la configurazione, oppure un array di file nel caso di file multipli
        for module in modules:
            self.selected_configs[module] = ""

    def importconfig(self, to_import):
        # importa un file tar con le configurazioni

        run = ["sudo","./src/scripts/tartoconf.sh"] + [to_import] + [os.getcwd() +"/src" ] + [os.getcwd() + "/src/configs"]
        subprocess.call(run)

    def exportconfig(self, exportpath, exportname):
        # esporta le configurazioni ad un file tar

        run = ["sudo","./src/scripts/conftotar.sh"] + [exportname] + [exportpath] + [os.getcwd()+"/src"] + ["configs"]
        subprocess.call(run)

    def apply_configs(self) -> bool:
        # funzione per applicare le configurazioni
        # ritorna 0 se non tutti i moduli sono stati selezionati, 1 se invece le impostazioni sono state applicate

        # controlla se per ogni modulo e stata selezionata una configurazione
        for module in self.selected_configs.keys():
            if self.selected_configs[module] == "":
                return False

        # applica i file di configurazione selezionati
        for module in self.modules:
            if module.is_multi_import:
                module.conf_import_multiple(self.selected_configs[module])

            else:
                module.conf_import(self.selected_configs[module])
            
            #print(module)
        

        return True

