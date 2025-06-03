#!/bin/bash

# === INSTALLER UNIVERSALE ===
set -e  # Termina lo script se si verifica un errore in qualsiasi comando

# 0. Verifica e installa Python 3.12 se necessario
if ! command -v python3.12 &> /dev/null
then
    echo "Python 3.12 non trovato. Procedo con l'installazione..."
    sudo apt update
    sudo apt install -y python3.12 python3.12-venv python3.12-distutils || { echo "❌ Errore installazione Python 3.12"; exit 1; }
else
    echo "Python 3.12 già installato."
fi

# 1. Configurazione automatica
APP_DIR="$(dirname "$(realpath "$0")")"  # Percorso assoluto della directory dello script
VENV_DIR="$HOME/.penguindeployer_venv"   # Directory ambiente virtuale Python
DESKTOP_FILE="$APP_DIR/Penguin-Deployer.desktop"  # Percorso file .desktop

# 2. Crea/aggiorna virtualenv
echo "Configurazione ambiente Python..."
python3.12 -m venv "$VENV_DIR" || { echo "❌ Errore creazione virtualenv"; exit 1; }
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"

# 3. Imposta permessi automaticamente
echo "Configurazione permessi..."
chmod 755 "$APP_DIR/app.sh"
chmod 755 "$APP_DIR/src/main.py"
find "$APP_DIR" -type f -name "*.py" ! -name "main.py" -exec chmod 644 {} \;

# 4. Crea desktop file
echo "Creazione launcher desktop..."
cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Version=1.0
Name=Penguin Deployer
Exec=$VENV_DIR/bin/python $APP_DIR/src/main.py
Icon=$APP_DIR/src/icon/icon.png
Path=$APP_DIR
Type=Application
Terminal=true
EOL

# 5. Installazione launcher
echo "Installazione..."
mkdir -p ~/.local/share/applications
ln -sf "$DESKTOP_FILE" ~/.local/share/applications/$(basename "$DESKTOP_FILE")
update-desktop-database ~/.local/share/applications

echo "Installazione completata! Cerca 'Penguin Deployer' nel menu applicazioni o esegui il launcher manualmente."
