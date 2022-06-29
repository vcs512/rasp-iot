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