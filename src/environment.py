import subprocess
import os
from Module import Module


class EnvironmentLogic(Module):
    def __init__(self, nconfigfolder):
        super().__init__(nconfigfolder)
        
        self.editor = ""  # nome dell'editor da impostare
        self.prompt = ""  # stringa del prompt da impostare
        self.hostname = ""  # hostname da impostare
        self.gconfigs = False  # flag per decidere se importare/esportare/applicare le impostazioni di gnome
        self.gconfigs_filename = ""  # nome del file su cui le configurazioni di gnome sono salvate

        self.mname = "environment"
        self.is_multi_import = False

    def debug(self, message):
        print(f"\033[94m[DEBUG]\033[0m {message}")  # Blu

    def set_env_configs(self):
        # imposta le configurazioni di ambiente in base alle variabili

        if self.editor:
            self.debug(f"Cambio editor: {self.editor}")
            subprocess.run(["sudo","./src/scripts/change_editor.sh", self.editor], check=True)
        else:
            self.debug("Editor non specificato, salto.")

        if self.prompt:
            self.debug(f"Cambio prompt: {self.prompt}")
            subprocess.run(["sudo","./src/scripts/change_prompt.sh", self.prompt], check=True)
        else:
            self.debug("Prompt non specificato o vuoto, salto.")

        if self.hostname:
            self.debug(f"Cambio hostname: {self.hostname}")
            subprocess.run(["sudo","./src/scripts/change_hostname.sh", self.hostname], check=True)
        else:
            self.debug("Hostname non specificato, salto.")

        if self.gconfigs and self.gconfigs_filename:
            self.debug(f"Import Gnome configs da: {self.gconfigs_filename}")
            subprocess.run(["./src/scripts/expimp_gconfigs.sh", "imp", self.gconfigs_filename], check=True)
        else:
            self.debug("Gnome configs non attivo o filename mancante, salto.")

    def conf_export(self, filename):
        full_config_path = os.path.join(self.configfolder, filename)

        # Generate GNOME configs filename
        if filename.endswith(".config"):
            base_name = filename[:-7]
        else:
            base_name = os.path.splitext(filename)[0]
            
        self.gconfigs_filename = os.path.join(self.configfolder, base_name)

        with open(full_config_path, 'w') as confexp:
            confexp.write("\neditor:" + self.editor)
            confexp.write("\nhostname:" + self.hostname)
            confexp.write("\ngconfigs:" + str(self.gconfigs))
            confexp.write("\ngconfigs_filename:" + self.gconfigs_filename)
            confexp.write("\n" + self.prompt)

        if self.gconfigs:
            subprocess.run(["./src/scripts/expimp_gconfigs.sh", "exp", self.gconfigs_filename], check=True)

    def conf_import(self, filename):
        full_config_path = os.path.join(self.configfolder, filename)

        with open(full_config_path) as conf:
            self.editor = conf.readline().strip("\n").split(":", 1)[1]
            self.hostname = conf.readline().strip("\n").split(":", 1)[1]
            self.gconfigs = conf.readline().strip("\n").split(":", 1)[1] == "True"
            self.gconfigs_filename = conf.readline().strip("\n").split(":", 1)[1]
            last_line = conf.readline()
            self.prompt = last_line.strip("\n") if last_line else ""

    def configure(self):
        self.set_env_configs()

    def __str__(self):
        return f"Environment Module: {self.mname}\n" \
               f"Editor: {self.editor}\n" \
               f"Prompt: {self.prompt}\n" \
               f"Hostname: {self.hostname}\n" \
               f"Gnome Configs Enabled: {self.gconfigs}\n" \
               f"Gnome Configs Filename: {self.gconfigs_filename}"
