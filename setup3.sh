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
chmod 755 "$APP_DIR/app.sh"  # Rende eseguibile lo script di installazione
chmod 755 "$APP_DIR/src/main.py"  # Rende eseguibile il file principale Python
find "$APP_DIR" -type f -name "*.py" ! -name "main.py" -exec chmod 644 {} \;  # Imposta permessi di lettura/scrittura per gli altri script Python (escluso main.py)

# 4. Crea desktop file (https://www.youtube.com/watch?v=9CTmC5Y7QeM&t=4s)
echo "Creazione launcher desktop..."
cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Version=1.0
Name=Penguin Deployer  # Nome che apparirà nel menu applicazioni
Exec=$VENV_DIR/bin/python $APP_DIR/src/main.py  # Comando per eseguire il programma principale usando il venv
Icon=$APP_DIR/src/icon/icon.png  # Icona dell'applicazione
Path=$APP_DIR  # Directory di lavoro quando si avvia l'app
Type=Application  # Tipo di lanciatore
Terminal=true  # Apro il terminale, per debug
EOL

# 5. Installazione
echo "Installazione..."
mkdir -p ~/.local/share/applications  # Crea la cartella locale per i file desktop se non esiste
# Crea un collegamento simbolico al file desktop nella cartella applicazioni utente per rendere disponibile il launcher nel menu
ln -sf "$DESKTOP_FILE" ~/.local/share/applications/$(basename "$DESKTOP_FILE")

# Aggiorna il database delle applicazioni per riconoscere il nuovo launcher
update-desktop-database ~/.local/share/applications

echo "Installazione completata! Cerca 'Penguin Deployer' nel menu applicazioni o semplicemente esegui Penguin-Deployer.desktop all'interno dell folder"