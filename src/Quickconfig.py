import os
import shutil


class QuickConfig():

    selected_configs: dict

    def __init__(self, modules):
        self.modules = modules
        self.selected_configs = {}

        # inserisci i moduli in un dizionario, per poi associare ad ogni modulo
        # un file selezionato per la configurazione, oppure un array di file nel caso di file multipli
        for module in modules:
            self.selected_configs[module] = ""

    def importconfig(self, to_import):
        import tarfile

        extract_temp_path = os.path.join(os.getcwd(), "temp_import_config")
        os.makedirs(extract_temp_path, exist_ok=True)

        # Pulisce prima il contenuto se già esiste
        for f in os.listdir(extract_temp_path):
            fpath = os.path.join(extract_temp_path, f)
            if os.path.isdir(fpath):
                shutil.rmtree(fpath)
            else:
                os.remove(fpath)

        # Estrai in temp
        with tarfile.open(to_import, "r") as tar:
            tar.extractall(path=extract_temp_path)

        # Sposta manualmente il contenuto da temp/configs/ a ./configs/
        src_config_dir = os.path.join(extract_temp_path, "configs")
        dest_config_dir = os.path.join(os.getcwd(), "configs")

        for item in os.listdir(src_config_dir):
            src_path = os.path.join(src_config_dir, item)
            dest_path = os.path.join(dest_config_dir, item)

            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)

        shutil.rmtree(extract_temp_path)  # Cleanup


    def exportconfig(self, exportpath):
        #esporta le configurazioni

        #crea un archivio tar

        here = os.getcwd()
        shutil.make_archive("export", "tar", here + "/configs")

        #mettilo nella cartella desirata
        shutil.move(here + "/export.tar", exportpath)

    def apply_configs(self) -> bool:
        #funzione per applicare le configurazioni
        #ritorna 0 se non tutti i moduli sono stati selezionati, 1 se invece le impostazioni sono state applicate
        
        #controlla se per ogni modulo e stata selezionata una configurazione
        for module in self.selected_configs.keys():
            if self.selected_configs[module] == "":
                return False

        #applica i file di configurazione selezionati
        for module in self.modules:
            if module.is_multi_import:
                module.conf_import_multiple(self.selected_configs[module])
            else:
                module.conf_import(self.selected_configs[module])

        return True

    #Nota: per l'aggiunta additiva di programmi alla lista di programmi, basterebbe aggiungere una funzione
    #di import che non resetta


'''
q = QuickConfig()

q.exportconfig("test")

print("\n" + os.getcwd())
q.importconfig(os.getcwd() + "/test/export.tar")
'''
