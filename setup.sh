#!/bin/bash

# === INSTALLER UNIVERSALE ===
set -e  # Exit on error

# 1. Configurazione automatica
APP_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$HOME/.penguindeployer_venv"
DESKTOP_FILE="$APP_DIR/Penguin-Deployer.desktop"

# 2. Crea/aggiorna virtualenv
echo "Configurazione ambiente Python..."
python3 -m venv "$VENV_DIR" || { echo "❌ Errore creazione virtualenv"; exit 1; }
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"

# 3. Imposta permessi automaticamente
echo "Configurazione permessi..."
chmod 755 "$APP_DIR/install.sh"
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
Terminal=false
EOL

# 5. Installazione
echo "Installazione..."
mkdir -p ~/.local/share/applications
# Collegamento simbolico al desktop file (per avere launcher aggiornato)
ln -sf "$DESKTOP_FILE" ~/.local/share/applications/$(basename "$DESKTOP_FILE")

# Aggiorna database delle applicazioni
update-desktop-database ~/.local/share/applications

echo "Installazione completata! Cerca 'Penguin Deployer' nel menu applicazioni."