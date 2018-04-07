#!/bin/sh
ssh cfisher5@ssh.pythonanywhere.com '
cd GLeague-Predictions/
git reset --hard
git pull
python3 reload.py
'