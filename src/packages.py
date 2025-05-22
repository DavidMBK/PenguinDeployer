import subprocess
from module import Module


class Packages(Module):
    selected_file: str

    def install_packages(self,packages):
        run = ["./src/scripts/install.sh"] + packages
        sub = subprocess.call(run)
        return sub

    def unistall_packages(self,packages):
        run = ["./src/scripts/uninstall.sh"] + packages
        sub = subprocess.call(run)
        return sub

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

""" Testing
if __name__ == "__main__":
    p = Packages()
    test_packages = ["curl", "vim"]

    print("Installazione")
    install_result = p.install_packages(test_packages)
    print(f"Installato: {install_result}")

    print("Disinstallazione")
    uninstall_result = p.unistall_packages(test_packages)
    print(f"Disinstallato: {install_result}")
"""