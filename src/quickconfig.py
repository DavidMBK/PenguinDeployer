import os
import shutil


class QuickConfig():

    def __init__(self, modules):
        self.modules = modules

    def importconfig(self, to_import):
        shutil.unpack_archive(to_import, os.getcwd() + "/configs", "tar", )

    def exportconfig(self, exportpath):
        #esporta le configurazioni

        #crea un archivio tar

        here = os.getcwd()
        shutil.make_archive("export", "tar", here + "/configs")

        #mettilo nella cartella desirata
        shutil.move(here + "/export.tar", exportpath)

    def apply_configs(self):
        #applica i file di configurazione selezionati

        #codice non finito, migliorare dopo
        for module in self.modules:
            module.conf_import()

    #Nota: per l'aggiunta additiva di programmi alla lista di programmi, basterebbe aggiungere una funzione
    #di import che non resetta


'''
q = QuickConfig()

q.exportconfig("test")

print("\n" + os.getcwd())
q.importconfig(os.getcwd() + "/test/export.tar")
'''
