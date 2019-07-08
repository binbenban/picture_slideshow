#!/bin/bash
sudo pkill -f feh
cd /home/pi/picture_slideshow
sudo python run_cli.py
feh --quiet -F -Z -Y -D 5.0 data/downloaded_images
# sudo reboot