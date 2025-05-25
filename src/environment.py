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
        confexp.write("\n editor:" + self.editor)
        confexp.write("\n prompt:" + self.prompt)
        confexp.write("\n hostname:" + self.hostname)
        confexp.write("\n gconfigs:" + str(self.gconfigs))
        confexp.write("\n gconfigs_filename:" + filename)

        if self.gconfigs:
            run = ["./src/scripts/expimp_gconfigs.sh"] + ["exp"] + [filename]
            subprocess.call(run)

    def conf_import(self, filename):

        conf = open(self.configfolder + "/" + filename)
        envs = conf.read()
        esplit = re.split(':|\n', envs)

        self.shell = esplit[1]
        self.editor = esplit[3]
        self.prompt = esplit[5]
        self.hostname = esplit[7]
        self.gconfigs = bool(esplit[9])
        self.gconfigs_filename = esplit[11]

    def configure(self):
        self.set_env_configs()


#shells cat /etc/shells to find them, then pick one and use chsh
#same thing for editor
#prompt takes as input a string.
#hostname takes as input a string aswell
#export gnome configs



if __name__ == "__main__":
    e = Environment()

    #testing import
    e.conf_import("src/configs/services/testconfig.config")

    #testing export
    e.conf_export("src/configs/services/testconfigexp.config")

    #testing configuration
    #e.configure()

