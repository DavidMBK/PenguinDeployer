#!/bin/bash

APP_DIR="$(dirname "$(realpath "$0")")" # Ottiene il percorso assoluto della directory dove si trova lo script,

VENV_DIR="$HOME/.penguindeployer_venv" # Percorso venv

REQUIREMENTS_FILE="$APP_DIR/requirements.txt" # Percorso del file requirements.txt

MAIN_SCRIPT="$APP_DIR/src/main.py" # Percorso main.py


if [ ! -d "$VENV_DIR" ]; then  # Controlla se venv esiste
    echo "[INFO] Creo ambiente virtuale in $VENV_DIR" 
    python3 -m venv "$VENV_DIR" # Crea venv se non esiste in venv_dir
    "$VENV_DIR/bin/pip" install --upgrade pip # Aggiorno pip
    "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS_FILE" # Installo tutte le pipeline di requirements.txt su venv_dir
fi


echo "[INFO] Avvio Penguin Deployer..."
exec "$VENV_DIR/bin/python" "$MAIN_SCRIPT"
# runno tramite venv
