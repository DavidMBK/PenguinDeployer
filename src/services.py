import subprocess

from module import Module
import re


class Services(Module):
    selected_file: str

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

    def conf_export(self, configurations, filename):
        #aggiornare nel futuro
        pass

    def conf_import(self, filename):
        self.selected_file = filename
        pass

    def configure(self):

        conf = open(self.selected_file)
        services = conf.read()
        split = re.split(':|\n', services)

        i = 0
        while i < len(split) / 2:
            self.service_onoff(split[i],split[i+1])
            i += 2


s = Services()
s.conf_import("configs/services.config")
s.configure()
