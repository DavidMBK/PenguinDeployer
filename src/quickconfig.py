import os
import shutil

class QuickConfig():

    def importconfig(self):
        pass

    def exportconfig(self):
        #esporta le configurazioni

        #crea un archivio tar

        here = os.getcwd()
        shutil.make_archive("export","tar",here + "/configs")


'''

q = QuickConfig


'''