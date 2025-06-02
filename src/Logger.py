import subprocess      
import pam             
import threading       
import time            

class Login:
    def __init__(self):
        self.username = ""    
        self.password = ""    
        self.admin = False    # Flag se l'utente è amministratore (sudoer)

    # Metodo per autenticare l'utente tramite PAM
    def authenticate(self, username, password):
        auth = pam.pam()                              # Controlla se la password corrisponde all'user
        return auth.authenticate(username, password)  # Restituisce True/False

    # Controlla se l'utente appartiene al gruppo 'sudo'
    def check_admin(self, username):
        try:
            result = subprocess.check_output(['groups', username])  # Ottiene gruppi dell'utente
            return "sudo" in result.decode()                        # Verifica se è presente 'sudo'
        except subprocess.CalledProcessError:
            return None                                             

    # Esegue un comando con privilegi sudo
    def run_command_with_sudo(self, command):
        if not self.admin or not self.password:
            return None, "Accesso non autorizzato"  # Verifica se è autorizzato

        try:
            # Esegue il comando con sudo e passa la password tramite stdin
            process = subprocess.Popen(
                ['sudo', '-S'] + command.split(),          # -S accetta la password via stdin per evitare prompt con terminale 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(input=self.password.encode())  # Passa la password
            return stdout.decode(), stderr.decode()  # Ritorna output e errori decodificati
        except subprocess.CalledProcessError as e:
            return None, e.stderr.decode()

    # Mantiene attiva la sessione sudo eseguendo `sudo -v` periodicamente
    def keep_sudo_alive(self):
        while True:
            stdout, stderr = self.run_command_with_sudo("-v")  # -v rinnova timestamp sudo
            if stderr:
                break              
            time.sleep(60)        # Aspetta 60 secondi prima del prossimo rinnovo

    # Metodo principale per eseguire il login come amministratore
    def adminlogin(self, username, password):
        if self.authenticate(username, password):     # Prima verifica PAM; Se è corretto, salva username e password
            self.username = username 
            self.password = password
            self.admin = self.check_admin(username)   # Controlla se è sudoer

            if self.admin:
                # Tenta di verificare accesso sudo
                stdout, stderr = self.run_command_with_sudo("-v")
                if stderr:
                    # Se riesce, lancia il thread che tiene vivo sudo
                    threading.Thread(target=self.keep_sudo_alive, daemon=True).start()

            return True, "Login effettuato con successo"
        return False, "Credenziali non validi"       
