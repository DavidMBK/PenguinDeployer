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

    def conf_export(self, filename):

        confexp = open(self.configfolder + "/" + filename, 'w')

        confexp.write("shell:" + self.shell)
        confexp.write("\neditor:" + self.editor)
        confexp.write("\nhostname:" + self.hostname)
        confexp.write("\ngconfigs:" + str(self.gconfigs))
        confexp.write("\ngconfigs_filename:" + filename)
        confexp.write("\n" + self.prompt)

        if self.gconfigs:
            run = ["./src/scripts/expimp_gconfigs.sh"] + ["exp"] + [filename]

    def conf_import(self, filename):

        conf = open(self.configfolder + "/" + filename)

        self.shell = conf.readline().strip("\n").split(":")[1]
        self.editor = conf.readline().strip("\n").split(":")[1]
        self.hostname = conf.readline().strip("\n").split(":")[1]
        self.gconfigs = "True" if (conf.readline().strip("\n").split(":")[1] == "True") else "False"
        self.gconfigs_filename = conf.readline().strip("\n").split(":")[1]
        self.prompt = conf.readline().strip("\n")


    def configure(self):
        self.set_env_configs()


e = EnvironmentLogic("src/configs/environment")

e.conf_import("prova.config")

e.conf_export("prova.config")

e.configure()


