#!/bin/bash
sudo pkill -f feh
cd /home/pi/picture_slideshow
source venv/bin/activate
picshow run
feh --quiet -F -Z -Y -D 5.0 data/downloaded_images
# sudo reboot
