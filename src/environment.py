from module import Module

# Shell predefinita
# Prompt
# Editor predefinito
# Temi desktop (se disponibile)

class Environment(Module):

    def sys_read(self):
        #aggiungere dopo
        pass

    def conf_export(self, filename):
        pass

    def conf_import(self, filename):
        pass

    def configure(self):
        pass


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