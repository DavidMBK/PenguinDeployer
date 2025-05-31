

class Module:
    # classe base per i moduli, fatta per essere inheritata e non instanziata di per se.

    configfolder: str # cartella che contiene le configurazioni del modulo
    mname: str # nome del modulo

    def __init__(self, nconfigfolder):
        self.configfolder = nconfigfolder

    def conf_export(self, filename):
        # funzione per esportare le configurazioni a un file
        pass

    def conf_import(self, filename):
        # funzione per importare le configurazioni da un file
        pass

    def configure(self):
        # funzione per applicare le configurazioni scelte
        pass
