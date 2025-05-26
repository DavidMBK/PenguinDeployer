import subprocess
from Module import Module
import re


class ServicesLogic(Module):

    def __init__(self, nconfigfolder):
        super().__init__(nconfigfolder)

        self.to_enable = []
        self.to_disable = []

        self.is_multi_import = True

    def service_onoff(self, service: str, enable: bool):
        #attiva o disattiva un servizio

        if enable:
            run = ["./src/scripts/service_onoff.sh"] + ["enable"] +  [service]
        else:
            run = ["./src/scripts/service_onoff.sh"] +  ["disable"]  + [service]

        subprocess.call(run)

    def sys_read(self):
        path = ["./systemctl.sh"]
        result = subprocess.run(path, capture_output=True, text=True)

        return result.stdout

    def conf_export(self, filename):

        confexp = open(self.configfolder + "/" + filename, 'w')

        for pack in self.to_enable:
            confexp.write("\n" + pack + ":" + "enable")

        for pack in self.to_disable:
            confexp.write("\n" + pack + ":" + "disable")

    def conf_import(self, filename):

        conf = open(self.configfolder + "/" + filename)
        services = conf.read()
        ssplit = re.split(':|\n', services)

        i = 0
        while i < len(ssplit):
            if ssplit[i + 1] == "enable":
                self.to_enable.append(ssplit[i])
            elif ssplit[i + 1] == "disable":
                self.to_disable.append(ssplit[i])
            else:
                print("Errore nel file di configurazione")
            i += 2

    def conf_import_multiple(self, filenames):

        self.to_enable = []
        self.to_disable = []

        for filename in filenames:
            self.conf_import(filename)

    def configure(self):

        for service in self.to_enable:
            self.service_onoff(service, True)

        for service in self.to_disable:
            self.service_onoff(service, False)

    def debug(self):
        print(f'Abilitati: {self.to_enable}')
        print(f'Disabilitati: {self.to_disable}')



"""
if __name__ == "__main__":
    s = Services(src/configs/services)

    #testing import
    s.conf_import("testconfig.config")

    #testing export
    s.conf_export("testconfigexp.config")

    #testing configuration (install/uninstall)
    s.configure()
"""
