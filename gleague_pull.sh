#!/bin/sh
ssh cfisher5@ssh.pythonanywhere.com '
cd GLeague-Predictions/
git pull
python3 reload.py
'