#!/bin/bash

query="$1"
systemctl list-unit-files --type=service --no-pager --no-legend | awk '{print $1}' | grep -i "$query"
