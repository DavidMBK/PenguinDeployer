import re
from module import Module

# Shell predefinita
# Prompt
# Editor predefinito
# Temi desktop (se disponibile)

class Environment(Module):

    def __init__(self,configfolder):
        self.shell = ""
        self.editor = ""
        self.prompt = ""
        self.hostname = ""
        self.gconfigs = False
        self.configfolder = configfolder

    def sys_read(self):
        #aggiungere dopo
        pass

    def set_env_configs(self):
        pass

    def conf_export(self, filename):
        confexp = open(self.configfolder + "/" + filename, 'w')

        confexp.write("shell:" + self.shell)
        confexp.write("\n editor:" + self.editor)
        confexp.write("\n prompt:" + self.prompt)
        confexp.write("\n hostname:" + self.hostname)
        confexp.write("\n gconfigs:" + str(self.gconfigs))

        if self.gconfigs:
            run = ["./src/scripts/expimp_gconfigs.sh"] + ""
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

    def configure(self):
        pass


#shells cat /etc/shells to find them, then pick one and use chsh
#same thing for editor
#prompt takes as input a string.
#hostname takes as input a string aswell
#export gnome configs


'''
if __name__ == "__main__":
    e = Environment()

    #testing import
    e.conf_import("src/configs/services/testconfig.config")

    #testing export
    e.conf_export("src/configs/services/testconfigexp.config")

    #testing configuration (install/uninstall)
    e.configure()
'''