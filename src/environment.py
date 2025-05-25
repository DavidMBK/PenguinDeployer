import re
import subprocess

from module import Module


class Environment(Module):

    def __init__(self, nconfigfolder):
        super().__init__(nconfigfolder)
        self.shell = ""
        self.editor = ""
        self.prompt = ""
        self.hostname = ""
        self.gconfigs = False
        self.gconfigs_filename = ""

    def sys_read(self):
        pass

    def set_env_configs(self):

        runs = ["./src/scripts/change_shell.sh"] + [self.shell]
        subprocess.call(runs)

        rune = ["./src/scripts/change_editor.sh"] + [self.editor]
        subprocess.call(rune)

        runp = ["./src/scripts/change_prompt.sh"] + [self.prompt]
        subprocess.call(runp)

        runh = ["./src/scripts/change_hostname.sh"] + [self.hostname]
        subprocess.call(runh)

        if self.gconfigs:
            grun = ["./src/scripts/expimp_gconfigs.sh"] + ["imp"] + [self.gconfigs_filename]
            subprocess.call(grun)

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
            subprocess.call(run)

    def conf_import(self, filename):

        conf = open(self.configfolder + "/" + filename)

        self.shell = conf.readline().strip("\n").split(":")[1]
        print(self.shell)
        self.editor = conf.readline().strip("\n").split(":")[1]
        print(self.editor)
        self.hostname = conf.readline().strip("\n").split(":")[1]
        print(self.hostname)
        self.gconfigs = "True" if (conf.readline().strip("\n").split(":")[1] == "True") else "False"
        print(self.gconfigs)
        self.gconfigs_filename = conf.readline().strip("\n").split(":")[1]
        print(self.gconfigs_filename)
        self.prompt = conf.readline().strip("\n")
        print(self.prompt)

    def configure(self):
        self.set_env_configs()


if __name__ == "__main__":
    e = Environment("src/configs/environment")

    #testing import
    e.conf_import("testconfig.config")

    #testing export
    e.conf_export("testconfigexp.config")

    #testing configuration
    e.configure()
