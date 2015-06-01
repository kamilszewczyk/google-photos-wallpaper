# google-photos-wallpaper
Python script for Linux Mint that will change the wallpaper on desktop screen to random image downloaded from Google Photos every 30 seconds.
Should work with any Linux that is able to set wallpaper with gsettings application. It will automatically set wallpaper for first screen (not tested on multiple screens environment)

## Requirements
* Python 3.*
* client_secret.json present in directory (you can generate client_secret file in Google Developer Console)

## Installation
* Clone repository to folder (i.e. /home/user/.wallpaper)
* Run "pip install -r requirements.txt"
* Run "chmod +x wallpaper.py"

## Usage
Script is set up to work with cron, add

* * * * * export DISPLAY=:0 && /path/to/wallpaper.py

This will automatically change the template every minute.
To run script in shorter periods use this answer: http://stackoverflow.com/a/9619441/1078755

