import subprocess
from module import Module


class Packages(Module):


    def install_packages(self,packages):
        run = ["./install.sh"] + packages
        exec = subprocess.call(run)
        return exec

