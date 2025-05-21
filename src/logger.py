import subprocess # Per controllare i gruppi dell'utente
import getpass # Non mostra la password mentre la scrivi
import pam # Si interfaccia con il PAM per l'autenticazione

class Login:
    #classe che si occupa del log-in

    def __init__(self):
        #inizializza la classe
        self.username = ""
        self.password = ""
        self.admin = False

    def get_credentials(self):
        #Preleva le credenziali dell'utente
        self.username = input("Username: ")
        self.password = getpass.getpass("Password: ")
        return self.username, password

    def authenticate(self, username, password):
        #controlla se le credenziali sono corrette
        auth = pam()
        return auth.authenticate(username, password)

    def check_admin(self):
        #controlla se l'utente è admin
        try:
            result = subprocess.check_output(['groups', self.username]) # Controlla i gruppi dell'utente.
            return "sudo" in result
        except subprocess.CalledProcessError:
        #se non riesce a controllare i gruppi dell'utente, ritorna Errore nel controllo
            return None

    def adminlogin(self):
        #funzione principale per il log-in
        print("Login Admin")
        username, password = self.get_credentials() # Preleva le credenziali.
    
        if self.authenticate(username, password):
            
            admin_check = self.check_admin(username) # Controllo se l'utente è admin.

            if admin_check is True:
                print("Login successful")
                self.admin = True
            else:
                print("User is not an admin")
                self.admin = False
        else:
            print("Unvalid credentials")
            self.admin = False