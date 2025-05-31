import subprocess
from Module import Module
import re
import os


class ServicesLogic(Module):

    def __init__(self, nconfigfolder):
        #inizializzazione
        super().__init__(nconfigfolder)

        self.to_enable = [] # lista dei servizi da abilitare
        self.to_disable = [] # lista dei servizi da disabilitare

        self.is_multi_import = True # flag per segnare che la classe importa più di un file alla volta

    def service_onoff(self, service: str, enable: bool):
        # attiva o disattiva un servizio

        if enable:
            run = ["./src/scripts/service_onoff.sh"] + ["enable"] + [service]
        else:
            run = ["./src/scripts/service_onoff.sh"] + ["disable"] + [service]

        subprocess.call(run)

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
        ssplit = list(filter(None, ssplit))

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
        # importa uno o più file

        self.to_enable = []
        self.to_disable = []

        for filename in filenames:
            self.conf_import(filename)

    def configure(self):
        # abilita e disabilita i servizzi

        for service in self.to_enable:
            self.service_onoff(service, True)

        for service in self.to_disable:
            self.service_onoff(service, False)

    def debug(self):
        print(f'Abilitati: {self.to_enable}')
        print(f'Disabilitati: {self.to_disable}')

    def find_service(self, query):
        comand = ["./src/scripts/systemctl.sh"] + [query]
        result = subprocess.run(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        matches = [m.strip() for m in result.stdout.strip().split("\n") if m.strip()]
        matches = [m.replace(".service", "") if m.endswith(".service") else m for m in matches]
        return matches
