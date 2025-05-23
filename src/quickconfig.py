import os
import shutil


class QuickConfig():

    def importconfig(self, to_import):
        shutil.unpack_archive(to_import,os.getcwd(),"tar",)

    def exportconfig(self, exportpath):
        #esporta le configurazioni

        #crea un archivio tar

        here = os.getcwd()
        shutil.make_archive("export", "tar", here + "/configs")

        #mettilo nella cartella desirata
        shutil.move(here + "/export.tar", exportpath)


q = QuickConfig()

q.exportconfig("test")

print("\n" + os.getcwd())
q.importconfig(os.getcwd() + "/test/export.tar")
