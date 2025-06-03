#!/bin/bash

# === INSTALLER UNIVERSALE ===
set -e  # Termina lo script se si verifica un errore in qualsiasi comando

# 1. Configurazione automatica
APP_DIR="$(dirname "$(realpath "$0")")"  # Ottiene il percorso assoluto della directory dello script, importante per .desktop
VENV_DIR="$HOME/.penguindeployer_venv"   # La directory dove verrà creato l'ambiente virtuale Python
DESKTOP_FILE="$APP_DIR/Penguin-Deployer.desktop"  # Percorso .dekstop 

# 2. Crea/aggiorna virtualenv
echo "Configurazione ambiente Python..."
python3 -m venv "$VENV_DIR" || { echo "❌ Errore creazione virtualenv"; exit 1; }  # Crea un ambiente virtuale Python, esce in caso di errore
"$VENV_DIR/bin/pip" install --upgrade pip  # Aggiorna pip nel venv
"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"  # installa pip requirements in venv

# 3. Imposta permessi automaticamente
echo "Configurazione permessi..."
chmod 755 "$APP_DIR/src/main.py"  # Rende eseguibile il file principale Python
find "$APP_DIR" -type f -name "*.py" ! -name "main.py" -exec chmod 644 {} \;  # Imposta permessi di lettura/scrittura per gli altri script Python (escluso main.py)

# 4. Crea desktop file
echo "Creazione launcher desktop..."
cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Version=1.0
Name=Penguin Deployer
Exec=$APP_DIR/app.sh
Icon=$APP_DIR/src/icon/icon.png
Path=$APP_DIR
Type=Application
Terminal=true
EOL

# Rendi il desktop file eseguibile
chmod +x "$DESKTOP_FILE"

# 5. Installazione launcher
echo "Installazione launcher..."
APPLICATIONS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPLICATIONS_DIR"

# Crea collegamento simbolico
ln -sf "$DESKTOP_FILE" "$APPLICATIONS_DIR/"

# Rendi app.sh eseguibile
chmod +x "$APP_DIR/app.sh"

# Aggiorna database desktop
update-desktop-database "$APPLICATIONS_DIR"

echo "✅ Installazione completata! Il launcher è pronto nel menu applicazioni"
echo "Puoi anche eseguire direttamente: ./app.sh"