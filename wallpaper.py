#!/usr/bin/env python3

from picasa import Picasa
import random
from os import listdir, remove
from os.path import isfile, join, dirname, realpath, exists
from subprocess import Popen, PIPE

picasa = Picasa()

refresh_frequency = 30
max_from_album = 10
current_dir = dirname(realpath(__file__))

# get list of all images from images directory
images = [f for f in listdir(current_dir + "/images") if isfile(join(current_dir + "/images", f))]
if (len(images) > 0):
    # get random image from retrieved images
    wallpaper = current_dir + "/images/" + random.choice(images)

    # get current wallpaper uri
    p = Popen('gsettings get org.cinnamon.desktop.background picture-uri', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    current_wallpaper = current_dir + "/images/" + "".join(p.stdout.read().decode("utf-8").split("/")[-1:]).strip(" \t\n\r'")

    # if the file exists in our images directory remove it
    if exists(current_wallpaper):
        remove(current_wallpaper)

    # set image to be new wallpaper
    Popen('gsettings set org.cinnamon.desktop.background picture-uri "file://' + wallpaper + '"', shell=True)

else:
    num_of_pictures = 3600 / refresh_frequency
    num_of_drawn = 0
    drawn = {}

    # draw random number of pictures from random album until we have enough pictures drawn
    album_list = picasa.get_album_list()
    while num_of_drawn < num_of_pictures:
        album = random.choice(album_list)
        if album["num_photos"] == 0:
            continue
        drawn_num = random.randint(1, max_from_album if album["num_photos"] > max_from_album else album["num_photos"])

        if (album["id"] in drawn):
            drawn[album["id"]] += drawn_num
        else:
            drawn[album["id"]] = drawn_num

        num_of_drawn += drawn_num

    # draw previosly set random of pictures from album
    for album_id in drawn:
        photos_list = random.sample(picasa.get_photos_list(album_id), drawn[album_id])

        for photo in photos_list:
            Picasa.get_photo(photo["src"], current_dir + "/images")

