#!/bin/bash

[ -z "$1" ] && exit 1

EDITOR_PATH=$(command -v "$1")
[ -z "$EDITOR_PATH" ] && exit 2

sudo update-alternatives --install /usr/bin/editor editor "$EDITOR_PATH" 100 >/dev/null 2>&1
sudo update-alternatives --set editor "$EDITOR_PATH" >/dev/null 2>&1
