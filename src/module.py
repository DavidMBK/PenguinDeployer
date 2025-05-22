
#classe base per i moduli, fatta per essere inheritata e non instanziata di per se.
class Module:

    def sys_read(self):
        #funzione per leggere le impostazioni attuali del sistema
        pass

    def conf_export(self, configurations, filename):
        #funzione per esportare le configurazioni a un file
        pass

    def conf_import(self, filename):
        #funzione per importare le configurazioni da un file
        pass

    def configure(self):
        #funzione per fare partile la configurazione del sistema
        pass
