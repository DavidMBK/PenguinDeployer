import subprocess
from module import Module


class Packages(Module):
    selected_file: str

    def install_packages(self,packages):
        run = ["./install.sh"] + packages
        exec = subprocess.call(run)
        return exec

    def unistall_packages(self,packages):
        run = ["./uninstall.sh"] + packages
        exec = subprocess.call(run)
        return exec

    def sys_read(self):
        #aggiornare nel futuro
        pass

    def conf_export(self, filename):
        #aggiornare nel futuro
        pass

    def conf_import(self, filename):
        self.selected_file = filename

    def configure(self):

        conf = open(self.selected_file)
        packs = conf.read()

        self.install_packages(packs)

