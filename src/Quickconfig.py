import os
import shutil


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
        shutil.unpack_archive(to_import, os.getcwd() + "/configs", "tar")

    def exportconfig(self, exportpath):
        # esporta le configurazioni ad un file tar

        here = os.getcwd()
        shutil.make_archive("export", "tar", here + "/configs")

        # mettilo nella cartella desiderata
        shutil.move(here + "/export.tar", exportpath)

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

        return True

