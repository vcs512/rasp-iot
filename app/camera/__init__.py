from flask import Blueprint

cam = Blueprint('cam', __name__)

from . import views


import os
#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#make videos directory to save videos
try:
    os.mkdir('./videos')
except OSError as error:
    pass


# try GPIO
gpio_ok = True

try:
    import RPi.GPIO as GPIO
except:
    gpio_ok = False

if gpio_ok:
    print('GPIO support OK!')
else:
    print('WARNING: GPIO in failsafe mode')


if gpio_ok:
    # Set up GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)