import subprocess
import pam
import threading
import time

class Login:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.admin = False

    def authenticate(self, username, password):
        auth = pam.pam()
        return auth.authenticate(username, password)

    def check_admin(self, username):
        try:
            result = subprocess.check_output(['groups', username])
            return "sudo" in result.decode()
        except subprocess.CalledProcessError:
            return None

    def run_command_with_sudo(self, command):
        if not self.admin or not self.password:
            return None, "Accesso non autorizzato"
            
        try:
            process = subprocess.Popen(
                ['sudo', '-S'] + command.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(input=self.password.encode())
            return stdout.decode(), stderr.decode()
        except subprocess.CalledProcessError as e:
            return None, e.stderr.decode()

    def keep_sudo_alive(self):
        while True:
            stdout, stderr = self.run_command_with_sudo("-v")
            if stderr:
                break
            time.sleep(60)

    def adminlogin(self, username, password):
        if self.authenticate(username, password):
            self.username = username
            self.password = password
            self.admin = self.check_admin(username)
            
            if self.admin:
                # Verifica che la password funzioni anche per sudo
                stdout, stderr = self.run_command_with_sudo("-v")
                if stderr:
                    threading.Thread(target=self.keep_sudo_alive, daemon=True).start()
            
            return True, "Login effettuato con successo"
        return False, "Credenziali non validi"
