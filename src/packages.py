import subprocess
from core/module


class Packages(Module):

    def install_packages(self,packages):
        run = ["./install.sh"] + packages
        exec = subprocess.call(run)
        return exec

    def unistall_packages(self,packages):
        run = ["./uninstall.sh"] + packages
        exec = subprocess.call(run)
        return exec

