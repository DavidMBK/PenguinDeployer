#!/bin/bash

tar -czf "$1" -C "$3" "$4"
mv "$1" "$2"