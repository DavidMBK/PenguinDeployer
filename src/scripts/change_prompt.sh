#!/bin/bash

[ -z "$1" ] && exit 1

PROMPT="$1"
sed -i '/^export PS1=/d' ~/.bashrc
echo "export PS1=\"$PROMPT\"" >> ~/.bashrc
