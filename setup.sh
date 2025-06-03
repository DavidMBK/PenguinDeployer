#!/bin/bash

# === INSTALLER UNIVERSALE ===
set -e  # Termina lo script se si verifica un errore in qualsiasi comando

# 1. Configurazione automatica
APP_DIR="$(dirname "$(realpath "$0")")"  # Ottiene il percorso assoluto della directory dello script, importante per .desktop
VENV_DIR="$HOME/.penguindeployer_venv"   # La directory dove verrà creato l'ambiente virtuale Python
DESKTOP_FILE="$APP_DIR/Penguin-Deployer.desktop"  # Percorso .dekstop 

# 1. Verifica Python 3.12 specificamente
PYTHON_VERSION_REQUIRED="3.12.3"
PYTHON_CMD="python3.12.3"

if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo "Python $PYTHON_VERSION_REQUIRED non trovato"
    
    if command -v python3 &> /dev/null; then
        CURRENT_VERSION=$(python3 --version | cut -d' ' -f2)
        echo "⚠ Trovata versione $CURRENT_VERSION invece di $PYTHON_VERSION_REQUIRED"
    fi
    
    if command -v apt-get &> /dev/null; then
        echo "Installazione Python $PYTHON_VERSION_REQUIRED e venv..."
        sudo apt-get update
        
        # Prima prova a installare il pacchetto completo
        if ! sudo apt-get install -y "python$PYTHON_VERSION_REQUIRED" "python$PYTHON_VERSION_REQUIRED-venv"; then
            echo "❌ Pacchetto ufficiale non disponibile, provo con deadsnakes PPA..."
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y "python$PYTHON_VERSION_REQUIRED" "python$PYTHON_VERSION_REQUIRED-venv" || {
                echo "❌ Fallita installazione Python $PYTHON_VERSION_REQUIRED";
                echo "Soluzioni alternative:";
                echo "1. pyenv install 3.12.3";
                echo "2. Compilare da sorgente";
                exit 1;
            }
        fi
    else
        echo "❌ Sistema non basato su apt. Alternative:";
        echo "1. pyenv install 3.12.3";
        echo "2. Compilare da sorgente";
        exit 1
    fi
fi

# Verifica modulo venv
if ! "$PYTHON_CMD" -c "import ensurepip, venv" 2>/dev/null; then
    echo "❌ Modulo venv mancante per Python $PYTHON_VERSION_REQUIRED";
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y "python$PYTHON_VERSION_REQUIRED-venv" || exit 1
    else
        echo "Installa manualmente il modulo venv per Python $PYTHON_VERSION_REQUIRED";
        exit 1
    fi
fi

# 1.2 Verifica/installa python3-tk
if ! dpkg -l python3-tk &> /dev/null && command -v apt-get &> /dev/null; then
    echo "Installazione dipendenza di sistema: python3-tk..."
    sudo apt-get install -y python3-tk || { echo "❌ Errore installazione python3-tk"; exit 1; }
fi

# 1.5 Verifica/installa dipendenze di sistema
if ! dpkg -l python3-tk &> /dev/null; then
    echo "Installazione dipendenza di sistema: python3-tk..."
    sudo apt-get install -y python3-tk || { echo "❌ Errore installazione python3-tk"; exit 1; }
fi

# 2. Crea/aggiorna virtualenv
echo "Configurazione ambiente Python $PYTHON_VERSION_REQUIRED..."
"$PYTHON_CMD" -m venv "$VENV_DIR" || { echo "❌ Errore creazione virtualenv"; exit 1; }  # Crea un ambiente virtuale Python, esce in caso di errore
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
