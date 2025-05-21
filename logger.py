import getpass
import subprocess
import pam

class Login:
    def __init__(self):
        self.username = ""
        self.admin = False

    def get_credentials(self):
        self.username = input("Username: ")
        password = getpass.getpass("Password: ")
        return self.username, password

    def authenticate_user(self, username, password):
        return pam().authenticate(username, password)

    def is_user_admin(self, username):
        try:
            result = subprocess.check_output(["groups", username], text=True)
            return "sudo" in result
        except subprocess.CalledProcessError:
            return None  # Errore nel controllo

    def adminlogin(self):
        print("🔐 Login Admin")
        username, password = self.get_credentials()

        if self.authenticate_user(username, password):
            admin_check = self.is_user_admin(username)
            if admin_check is True:
                print("✅ Accesso come admin riuscito.")
                self.admin = True
            elif admin_check is False:
                print("⚠️ L'autenticazione è riuscita, ma l'utente non è un amministratore.")
            else:
                print("❌ Errore nel controllo dei gruppi.")
        else:
            print("❌ Username o password non validi.")

# Esecuzione dello script
if __name__ == "__main__":
    login = Login()
    login.adminlogin()
