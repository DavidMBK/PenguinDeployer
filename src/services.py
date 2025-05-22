import subprocess

from module import Module
import re


class Services(Module):
    to_enable: list[str] = []
    to_disable: list[str] = []

    def service_onoff(self, service: str, enable: bool):
        #attiva o disattiva un servizio

        if enable:
            run = ["./service_onoff.sh"] + " enable " + service
        else:
            run = ["./service_onoff.sh"] + " disable " + service

        subprocess.call(run)

    def sys_read(self):
        path = ["./systemctl.sh"]
        result = subprocess.run(path, capture_output=True, text=True)

        return result.stdout

    def conf_export(self, filename):

        confexp = open(filename, 'w')

        for pack in self.to_enable:
            confexp.write("\n" + pack + ":" + "enable")

        for pack in self.to_disable:
            confexp.write("\n" + pack + ":" + "disable")

    def conf_import(self, filename):

        conf = open(filename)
        services = conf.read()
        ssplit = re.split(':|\n', services)

        i = 0
        while i < len(ssplit) / 2:
            if ssplit[i + 1] == "enable":
                self.to_enable.append(ssplit[i])
            elif ssplit[i + 1] == "disable":
                self.to_disable.append(ssplit[i])
            else:
                print("Errore nel file di configurazione")
            i += 2

    def configure(self):

        for service in self.to_enable:
            self.service_onoff(service, True)

        for service in self.to_disable:
            self.service_onoff(service, False)


""" Testing
if __name__ == "__main__":
    s = Servicess()

    #testing import
    s.conf_import("src/configs/services/testconfig.config")

    #testing export
    s.conf_export("src/configs/services/testconfigexp.config")

    #testing configuration (install/uninstall)
    s.configure()
"""
