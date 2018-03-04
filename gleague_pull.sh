#!/bin/sh
ssh cfisher5@ssh.pythonanywhere.com '
cd GLeaguePredictions/GLeague-Predictions/
git reset --hard
git pull
python3 get_gleague_data.py
'