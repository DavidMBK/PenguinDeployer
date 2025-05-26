import subprocess
import os
from Module import Module

class EnvironmentLogic(Module):
    def __init__(self, nconfigfolder):
        super().__init__(nconfigfolder)
        self.shell = ""
        self.editor = ""
        self.prompt = ""
        self.hostname = ""
        self.gconfigs = False
        self.gconfigs_filename = ""
        self.configfolder = nconfigfolder

    def sys_read(self):
        pass

    def set_env_configs(self):
        subprocess.run(["./src/scripts/change_shell.sh", self.shell], check=True)
        subprocess.run(["./src/scripts/change_editor.sh", self.editor], check=True)
        subprocess.run(["./src/scripts/change_prompt.sh", self.prompt], check=True)
        subprocess.run(["./src/scripts/change_hostname.sh", self.hostname], check=True)

        if self.gconfigs:
            subprocess.run(["./src/scripts/expimp_gconfigs.sh", "imp", self.gconfigs_filename], check=True)

    def conf_export(self, filepath):
        """Export configuration to specified filepath"""
        try:
            self.gconfigs_filename = f"{os.path.splitext(os.path.basename(filepath))[0]}_gconfigs.config"

            with open(filepath, 'w') as confexp:
                confexp.write(f"shell:{self.shell}\n")
                confexp.write(f"editor:{self.editor}\n")
                confexp.write(f"hostname:{self.hostname}\n")
                confexp.write(f"gconfigs:{str(self.gconfigs)}\n")
                confexp.write(f"gconfigs_filename:{self.gconfigs_filename}\n")
                confexp.write(f"prompt:{self.prompt}\n")

            if self.gconfigs:
                subprocess.run(["./src/scripts/expimp_gconfigs.sh", "exp", self.gconfigs_filename], check=True)
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")

    def conf_import(self, filepath):
        """Import configuration from specified filepath"""
        try:
            with open(filepath, 'r') as conf:
                for line in conf:
                    line = line.strip()
                    if not line or ":" not in line:
                        continue
                    key, value = line.split(":", 1)
                    if key == "shell":
                        self.shell = value
                    elif key == "editor":
                        self.editor = value
                    elif key == "hostname":
                        self.hostname = value
                    elif key == "gconfigs":
                        self.gconfigs = value == "True"
                    elif key == "gconfigs_filename":
                        self.gconfigs_filename = value
                    elif key == "prompt":
                        self.prompt = value
        except Exception as e:
            raise Exception(f"Import failed: {str(e)}")

    def configure(self):
        self.set_env_configs()
