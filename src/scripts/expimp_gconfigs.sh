#!/bin/bash

if [ "$1" = "imp" ] ; then
  dconf load / < "${2}gnco.txt"
else
  dconf dump / > "${2}gnco.txt"
