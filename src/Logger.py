import subprocess  # Per controllare i gruppi dell'utente
import getpass  # Non mostra la password mentre la scrivi
import pam  # Si interfaccia con il PAM per l'autenticazione
import threading
import time
import subprocess

# ! ATTENZIONE !#  USARE VENV.

class Login:
    # classe che si occupa del log-in

    def __init__(self):
        # inizializza la classe
        self.username = ""
        self.password = ""
        self.admin = False

    def get_credentials(self):
        # Preleva le credenziali dell'utente
        self.username = input("Username: ")
        self.password = getpass.getpass("Password: ")
        return self.username, self.password

    def authenticate(self, username, password):
        # controlla se le credenziali sono corrette
        auth = pam.pam()
        return auth.authenticate(username, password)

    def check_admin(self, username):
        # controlla se l'utente è admin
        try:
            result = subprocess.check_output(['groups', username])  # Controlla i gruppi dell'utente.
            return "sudo" in result.decode()
        except subprocess.CalledProcessError:
            # se non riesce a controllare i gruppi dell'utente, ritorna Errore nel controllo
            return None

    def sudo(self):
        subprocess.run(["sudo", "-v"])

    def keep_sudo_alive(self):
        while True:
            subprocess.run(["sudo", "-v"])
            time.sleep(60)  # Refresh every 60 seconds

    # Start it as a daemon thread after login
    threading.Thread(target=keep_sudo_alive, daemon=True).start()

    def adminlogin(self, username, password):
        # funzione principale per il log-in
        if self.authenticate(username, password):
            print('Avvio autenticazione')
            admin_check = self.check_admin(username)  # Controllo se l'utente è admin.

            if admin_check is True:
                self.admin = True
                self.sudo()
                self.keep_sudo_alive()
                return True, "Login Successful"
            else:
                self.admin = False
                return False, "User is not an admin"
        else:
            self.admin = False
            return False, "Unvalid credentials"
