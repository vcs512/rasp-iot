import cv2

def detect_face(frame):

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (linhas, colunas) = cinza.shape
    cinza = cv2.resize( cinza, (linhas//2, colunas//2) )
    frame = cv2.resize( frame, (colunas//4, linhas//4) )

# pouca acuracia
    # face_cascade = cv2.CascadeClassifier('./saved_model/haarcascade_frontalface_default.xml')
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(5,5), flags=cv2.CASCADE_SCALE_IMAGE)
    
    # for (x,y,w,h) in faces:
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    
# ====================================================================    
    # CNN    
    # #Load pretrained face detection model    
    # net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')
    # #global net
    # (h, w) = frame.shape[:2]
    # blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
    #     (300, 300), (104.0, 177.0, 123.0))   
    # net.setInput(blob)
    # detections = net.forward()
    # confidence = detections[0, 0, 0, 2]

    # if confidence < 0.5:            
    #         return frame           

    # box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    # (startX, startY, endX, endY) = box.astype("int")
    # try:
    #     #frame=frame[startY:endY, startX:
    #     cv2.rectangle(frame,(startX,startY),(endX,endY),(255,0,0),2)
        
    #     (h, w) = frame.shape[:2]
    #     r = 480 / float(h)
    #     dim = ( int(w * r), 480)
    #     frame=cv2.resize(frame,dim)
    # except Exception as e:
    #     pass


# ====================================================================
# testar processamento
    # haar_face_cascade = cv2.CascadeClassifier('./saved_model/haarcascade_frontalface_alt.xml')
    haar_face_cascade = cv2.CascadeClassifier('./saved_model/lbpcascade_frontalface.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return frame