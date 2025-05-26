import subprocess
from Module import Module
import re
import os


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
        if not os.path.isabs(filename):
            filename = os.path.join(self.configfolder, filename)

        with open(filename, 'w') as confexp:
            for pack in self.to_enable:
                confexp.write("\n" + pack + ":" + "enable")
            for pack in self.to_disable:
                confexp.write("\n" + pack + ":" + "disable")


    def conf_import(self, filename):
        if not os.path.isabs(filename):
            filename = os.path.join(self.configfolder, filename)

        try:
            with open(filename) as conf:
                for line_num, line in enumerate(conf, start=1):
                    line = line.strip()
                    if not line:
                        continue  # salta righe vuote
                    if ':' not in line:
                        print(f"Riga {line_num} ignorata: '{line}' non contiene ':'")
                        continue
                    name, action = map(str.strip, line.split(":", 1))
                    if action == "enable":
                        self.to_enable.append(name)
                    elif action == "disable":
                        self.to_disable.append(name)
                    else:
                        print(f"Riga {line_num} errore: azione non valida '{action}'")
        except FileNotFoundError:
            print(f"File non trovato: {filename}")
        except Exception as e:
            print(f"Errore durante l'importazione: {e}")

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


    def find_service(self, query):  
        comand = ["./src/scripts/systemctl.sh"] + [query]
        result = subprocess.run(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        matches = [m.strip() for m in result.stdout.strip().split("\n") if m.strip()]
        matches = [m.replace(".service", "") if m.endswith(".service") else m for m in matches]
        return matches


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
