#!/bin/bash

# === CONFIGURAZIONE ===
APP_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$HOME/.penguindeployer_venv"
REQUIREMENTS_FILE="$APP_DIR/requirements.txt"
MAIN_SCRIPT="$APP_DIR/src/main.py"

# === CREA VENV SE NON ESISTE CONFIGURAZIONE ROBUSTA === 
if [ ! -d "$VENV_DIR" ]; then
    echo "[INFO] Creo ambiente virtuale in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS_FILE"
fi

# === LANCIA L'APP ===
echo "[INFO] Avvio Penguin Deployer..."
exec "$VENV_DIR/bin/python" "$MAIN_SCRIPT"
