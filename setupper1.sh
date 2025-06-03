#!/bin/bash
# === PENGUIN DEPLOYER INSTALLER ===
set -e

# 1. Configurazione iniziale
APP_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$HOME/.penguindeployer_venv"
DESKTOP_FILE="$APP_DIR/Penguin-Deployer.desktop"
PYTHON_VERSION="3.12"
PYTHON_CMD="python3.12"

# 2. Installa dipendenze di sistema
if command -v apt-get &> /dev/null; then
    echo "⏳ Installazione dipendenze di sistema..."
    sudo apt-get update
    
    # Pacchetti essenziali
    sudo apt-get install -y \
        python3-pip \
        python3-tk \
        python3-venv \
        || { echo "❌ Errore installazione dipendenze base"; exit 1; }
    
    # Python 3.12 specifico
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        echo "⏳ Installazione Python $PYTHON_VERSION..."
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt-get update
        sudo apt-get install -y \
            "python$PYTHON_VERSION" \
            "python$PYTHON_VERSION-venv" \
            || { echo "❌ Fallita installazione Python $PYTHON_VERSION"; exit 1; }
    fi
else
    echo "⚠ Sistema non basato su apt - verifica manualmente:"
    echo "- python3-tk installato"
    echo "- python3-pip installato"
    echo "- python$PYTHON_VERSION installato"
fi

# 3. Crea/aggiorna virtualenv
echo "⏳ Configurazione ambiente virtuale..."
"$PYTHON_CMD" -m venv "$VENV_DIR" || { echo "❌ Errore creazione virtualenv"; exit 1; }
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"

# 4. Configurazione permessi
echo "⏳ Configurazione permessi..."
chmod 755 "$APP_DIR/app.sh"
chmod 755 "$APP_DIR/src/main.py"
find "$APP_DIR" -type f -name "*.py" ! -name "main.py" -exec chmod 644 {} \;

# 5. Creazione desktop file
echo "⏳ Creazione launcher desktop..."
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

chmod +x "$DESKTOP_FILE"

# 6. Installazione finale
APPLICATIONS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPLICATIONS_DIR"
ln -sf "$DESKTOP_FILE" "$APPLICATIONS_DIR/"
update-desktop-database "$APPLICATIONS_DIR"

echo "✅ Installazione completata!"
echo "- Avvia con: ./app.sh"
echo "- Oppure cerca 'Penguin Deployer' nel menu applicazioni"
echo "- Ambiente virtuale: $VENV_DIR"
