#!/bin/bash

echo "Pacchetti da rimuovere: $@"
sudo apt remove -y "$@"


