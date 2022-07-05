import cv2

def detect_face(frame,w,h, scaleFactor=1.0, minNeighbors=2):
    '''use cv to detect faces'''

    # HAAR cascade - better accuracy
    # haar_face_cascade = cv2.CascadeClassifier('./saved_model/haarcascade_frontalface_alt.xml')
    
    # LBP - fast
    haar_face_cascade = cv2.CascadeClassifier('./saved_model/lbpcascade_frontalface.xml')
    
    reduc = 4
    framer = cv2.resize( frame, (h//reduc, w//reduc) )
    gray = cv2.cvtColor(framer, cv2.COLOR_BGR2GRAY)
    faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (reduc*x, reduc*y), (reduc*x + reduc*w, reduc*y + reduc*h), (0, 0, 255), 2)

    return frame