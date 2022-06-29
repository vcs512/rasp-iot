# flask-WEB
from concurrent.futures import thread
from flask import Flask, render_template, Response, request, redirect, url_for, send_file
from flask_login import login_required, current_user
from . import cam

# permissions
from ..models import Permission, Role
from ..decorators import admin_required, permission_required

# thread for camera and servos
from threading import Thread

# saving archives in system
import datetime, time
import glob, re
import os, sys

# computer vision and camera
from itertools import count
import cv2
import numpy as np
from app.camera.visao import detect_face, motion

# servos control
from app.camera.servo import Servo_Control
from .forms import Controle_servo, Servo_H, Servo_V

# MQTT
from app.mqtt_func.mqtt_func import client
from app.mqtt_func import mqtt_func


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


# global interfunction variables
capture = False
dec_motion = False
dec_face = False
camera_on = False
rec = False
varre = False
varrendo = False
# controle = False
lock_servos = False

camera_device = 0

def gen_frames():  
    '''generator: generate frame by frame from camera'''

    global out, capture, rec_frame, varrendo, dec_motion, dec_face, varre

    while rec or camera_on:
        
        # recording
        if rec:
            try:
                _, buffer = cv2.imencode('.jpg', rec_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass



        # just see camera
        else:
            success, frame = camera.read()
            if success:
                (w,h,_) = frame.shape
                
                # modify frame with functions
                if dec_motion:
                    frame = motion.motion(frame, w,h)
                    
                if dec_face:
                    frame = detect_face.detect_face(frame, w,h)

                # save picture
                if capture:
                    capture = False
                    now = datetime.datetime.now()
                    p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                    cv2.imwrite(p, frame)

                # servo sweeping
                if varre:
                    # if varrendo:
                    if varrendo and th2.is_alive():
                        dec_motion = False
                        dec_face = False
                        varrendo = False
                    else:
                        th2 = Thread (target = Servo_Control.Varredura_Servos, args= (10,20) )
                        th2.start()
                        varrendo = True

                # return frame                    
                try:
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    pass
            


# this view uses the frame generator
@cam.route('/video_feed')
@login_required
def video_feed():
    if camera_on or rec:
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for('.index'))



# full main camera view
@cam.route('/camera', methods=['GET', 'POST'])
@login_required
def index():
    global camera_on, dec_face, dec_motion, rec, varre, lock_servos
    
    return render_template('camera/camera.html', camera_on = camera_on, rec = rec)


# computer vision view
@cam.route('/camera_cv', methods=['GET'])
@login_required
def camera_cv():
    global camera_on, dec_face, dec_motion, rec, varre
    
    return render_template('camera/cam-cv.html', camera_on = camera_on, rec = rec, dec_face = dec_face, dec_motion = dec_motion)


# servo control view
@cam.route('/servos', methods=['GET', 'POST'])
@login_required
def servos():
    global camera_on, rec, varre, lock_servos
    
    if gpio_ok:
        angulo_H = Servo_Control.Angulo_Atual_H()
        angulo_V = Servo_Control.Angulo_Atual_V()
    else:
        angulo_H = -180
        angulo_V = -180

    # form = Controle_servo()

    # if request.method == 'POST':
    #     if form.submit_H.data == True:
    #         angulo_H = form.angulo_H.data
    #         print('H = ', angulo_H)
    #         Servo_Control.Controle_Manual_H(angulo_H=angulo_H,slp=1)
        
    #     elif form.submit_V.data == True:
    #         angulo_V = form.angulo_V.data
    #         Servo_Control.Controle_Manual_V(angulo_V=angulo_V,slp=1)

    #     else:
    #         angulo_H = form.angulo_H.data
    #         angulo_V = form.angulo_V.data
            
    #         Servo_Control.Controle_Manual(angulo_H=angulo_H,angulo_V=angulo_V,slp=1)

    #     return redirect(url_for(cam.servos))

    formH = Servo_H()
    formV = Servo_V()
    
    if formH.validate_on_submit():
        angulo_H = formH.angulo_H.data
        Servo_Control.Controle_Manual_H(angulo_H=angulo_H,slp=1)

    if formV.validate_on_submit():
            angulo_V = formV.angulo_V.data
            Servo_Control.Controle_Manual_V(angulo_V=angulo_V,slp=1)

    
    return render_template('camera/cam-servos.html', camera_on = camera_on, rec = rec, varre=varre, lock_servos=lock_servos, angulo_H=angulo_H, angulo_V=angulo_V, formH=formH, formV=formV)



@cam.route('/cam_adm',methods=['POST','GET'])
@login_required
@permission_required(Permission.ADMIN)
def teste():
    return 'so adm'


# function to record videos
def cam_record():
    global rec, rec_frame, rec_status, camera, camera_on
    rec = True

    print('Openning VideoCapture inside the thread')
    if not camera_on:
        camera = cv2.VideoCapture(camera_device)

    # Check if camera opened successfully
    while not camera.isOpened():
        print(f'Unable to read camera feed camera={camera}')
        if not rec:
            return

    # get a valid frame to determine properties
    for i in count(1):
        print(f'Trying to read (i={i})...')
        ret, _ = camera.read()
        if ret:
            break
        if not rec:
            return

    # Default resolutions of the frame are obtained.
    # The default resolutions are system dependent.
    frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(camera.get(cv2.CAP_PROP_FPS))
    print(f'frame_rate={frame_rate}, frame_width={frame_width}, frame_height={frame_height}')
    
    # Define the codec and create VideoWriter object. 
    # The output is stored in 'output.avi' file.
    now = datetime.datetime.now()
    out = cv2.VideoWriter('videos/vid_{}.avi'.format(str(now).replace(":",'')), cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width, frame_height))

    while True:
      rec_status, rec_frame = camera.read()
      if rec_status:
        # Write the frame into the file 'output.avi'
        out.write(rec_frame)
        if not rec:
          break
    
    # release the video capture and video write objects
    if not camera_on:
        camera.release()
    out.release()



# view to intermediate requests
# return referrer url
@cam.route('/cam_requests',methods=['POST','GET'])
@login_required
def tasks():
    global camera_on,camera, capture, dec_motion, dec_face, rec, varre, lock_servos
    print('Entering cam_requests')
    if request.method == 'POST':
        
        # take a picture
        if request.form.get('click'):
            capture = True

        # see controls panel
        # elif  request.form.get('stop_controls'):
        #     controle = False
        # elif  request.form.get('controls'):
        #     controle = True

        # motion detection
        elif  request.form.get('no_motion'):
            dec_motion = False
        elif  request.form.get('dec_motion'):
            dec_motion = True
        
        # face detection
        elif  request.form.get('no_face'):
            dec_face = False
        elif  request.form.get('dec_face'):
            dec_face = True



        # arrow fine servo
        elif  request.form.get('left'):
            angulo_H = Servo_Control.Angulo_Atual_H()
            # print('angulo = ', angulo_H)
            Servo_Control.Controle_Manual_H(angulo_H-10,slp=1)
        elif  request.form.get('right'):
            angulo_H = Servo_Control.Angulo_Atual_H()
            # print('angulo = ', angulo_H)
            Servo_Control.Controle_Manual_H(angulo_H+10,slp=1)

        elif  request.form.get('down'):
            angulo_V = Servo_Control.Angulo_Atual_V()
            Servo_Control.Controle_Manual_V(angulo_V+10,slp=1)
        elif  request.form.get('up'):
            angulo_V = Servo_Control.Angulo_Atual_V()
            Servo_Control.Controle_Manual_V(angulo_V-10,slp=1)


        # servo sweep
        elif  request.form.get('para_varredura'):
            varre = False
        elif  request.form.get('varrer'):
            varre = True

        # lock servos
        elif  request.form.get('open_servos'):
            lock_servos = False
        elif  request.form.get('lock_servos'):
            lock_servos = True
        
            
        
        # see camera image
        elif  request.form.get('start'):
            if not camera_on and not rec:
                camera = cv2.VideoCapture(camera_device)
                mqtt_func.publish(client, 'abriu camera')
            camera_on = True
        elif  request.form.get('stop'):
            if camera_on and not rec:
                camera.release()
            camera_on = False
        
        # recording
        elif request.form.get('rec_start'):
            if not rec:
                #Start new thread for recording the video
                th = Thread(target = cam_record)
                th.start()
                time.sleep(1)
        elif request.form.get('rec_stop'):
            if rec:
                rec = False
                time.sleep(1)
    print('Leaving cam_requests')
    # return redirect(url_for('.index'))
    return redirect(request.referrer)



# about project
@cam.route('/tabela',methods=['POST','GET'])
def tabela():
    return render_template('camera/tabela.html')






@cam.route('/files',methods=['POST','GET'])
@login_required
def files():
    fns = glob.glob('videos/*.avi')
    if fns != []:
        fns = list(map(lambda x: x.lstrip('videos').lstrip('/'), fns))
        dates = list(map(lambda x: re.search(r'[0-9]+-[0-9]+-[0-9]+', x).group(0), fns))
        times = list(map(lambda x: re.search(r' [0-9]+\.[0-9]+.avi$', x).group(0).lstrip().rstrip('.avi'), fns))
        d = list(map(lambda x, y, z: list([x, y, z]), fns, dates, times))
    else:
        d = []
    return render_template('camera/files.html', data = d)

@cam.route('/file_action',methods=['POST'])
@login_required
def file_action():
    if request.form.get('download'):
        print('download')
        fn = 'vid_{} {}.avi'.format(request.form.get('date'), request.form.get('time'))
        print(f'fn={fn} getenv("PWD")={os.getenv("PWD")}')
        try:
            return send_file('../videos/' + fn)
        except Exception as e:
            print(str(e))
    if request.form.get('erase'):
        fn = 'videos/vid_{} {}.avi'.format(request.form.get('date'), request.form.get('time'))
        print('erase')
        print(f'fn={fn}')
        os.unlink(fn)
    return redirect(url_for('cam.files'))
