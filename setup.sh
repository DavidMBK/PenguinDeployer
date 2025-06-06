#!/bin/bash
# === PENGUIN DEPLOYER INSTALLER ===
set -e # Termina lo script in caso di errore

# 1. Configurazione iniziale
APP_DIR="$(dirname "$(realpath "$0")")" # Directory dell'applicazione
VENV_DIR="$HOME/.penguindeployer_venv" # Directory del virtualenv
PYTHON_VERSION="3.12"
PYTHON_CMD="python3.12"

# 2. Installa dipendenze di sistema
if command -v apt-get &> /dev/null; then # Controlla se apt-get è disponibile
    echo "Installazione dipendenze di sistema..."
    sudo apt-get update
    
    # Pacchetti essenziali pip, tkinter e virtualenv
    sudo apt-get install -y \
        python3-pip \
        python3-tk \
        python3-venv \
        || { echo "Errore installazione dipendenze base"; exit 1; } 
    
    # Installa Python 3.12 specifico se non presente
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        echo "Installazione Python $PYTHON_VERSION..."
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt-get update
        sudo apt-get install -y \
            "python$PYTHON_VERSION" \
            "python$PYTHON_VERSION-venv" \
            || { echo "Fallita installazione Python $PYTHON_VERSION"; exit 1; }
    fi
else
    echo "Sistema non basato su apt - verifica manualmente:"
    echo "- python3-tk installato"
    echo "- python3-pip installato"
    echo "- python$PYTHON_VERSION installato"
fi

# 3. Crea/aggiorna virtualenv
echo "Configurazione ambiente virtuale..."
"$PYTHON_CMD" -m venv "$VENV_DIR" || { echo "Errore creazione virtualenv"; exit 1; }
"$VENV_DIR/bin/pip" install --upgrade pip # Aggiorna pip all'ultima versione
"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt" # Installa le dipendenze del progetto nella virtualenv

# 4. Configurazione permessi
echo "Configurazione permessi..."
chmod 755 "$APP_DIR/app.sh" 
chmod 755 "$APP_DIR/src/main.py"
find "$APP_DIR" -type f -name "*.py" ! -name "main.py" -exec chmod 644 {} \;

# 5. Creazione desktop file
echo "Creazione launcher desktop..."
USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6) # Ottiene la home directory dell'utente che ha eseguito lo script /etc/nsswitch.conf - passwd - "es. David"
DESKTOP_DIR="$USER_HOME/Desktop" # Directory del Desktop dell'utente, es "/home/david/Desktop"

# Crea cartella Desktop se non esiste
mkdir -p "$DESKTOP_DIR" # -p per indicare di non dare errore se la cartella esiste già

DESKTOP_FILE="$DESKTOP_DIR/Penguin-Deployer.desktop"

# Crea il desktop file con attributo trusted incluso
echo "[Desktop Entry]" > "$DESKTOP_FILE"
echo "Version=1.0" >> "$DESKTOP_FILE"
echo "Name=Penguin Deployer" >> "$DESKTOP_FILE"
echo "Exec=$APP_DIR/app.sh" >> "$DESKTOP_FILE"
echo "Icon=$APP_DIR/src/icon/icon.png" >> "$DESKTOP_FILE"
echo "Path=$APP_DIR" >> "$DESKTOP_FILE"
echo "Type=Application" >> "$DESKTOP_FILE"
echo "Terminal=true" >> "$DESKTOP_FILE"
echo "Trusted=true" >> "$DESKTOP_FILE"  # Forza trusted status non troppo funzionante

# Imposta permessi corretti
chown "$SUDO_USER:" "$DESKTOP_FILE" # Cambia il proprietario del file al SUDO_USER
chmod 755 "$DESKTOP_FILE" # Imposta permessi di esecuzione, manca solo Allow launching

echo "Installazione completata!"
echo "-Launcher creato sul Desktop: $DESKTOP_FILE" 
echo "Abilitare l'allow launching con tasto destro sul file desktop ed eseguirlo"
echo "-Ambiente virtuale: $VENV_DIR"
