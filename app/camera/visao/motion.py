# https://automaticaddison.com/motion-detection-using-opencv-on-raspberry-pi-4/ 

import cv2
import numpy as np

def motion(frame,w,h, back_sub, reduc=2, history=50, dk=50):
    '''use cv to detect motion
    
    history: large = more robust to movement
    dk:      small = detect minor objects movement
    '''

    # back_sub = cv2.createBackgroundSubtractorMOG2(history=history, varThreshold=25, detectShadows=True)

    # kernel for morphological operation
    #                     sensitivity
    # big dimensions:          -
    # small dimensions:        +
    kernel = np.ones((dk,dk),np.uint8)

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cinza = cv2.resize( cinza, (h//reduc, w//reduc) )
    
    # create foreground mask
    fg_mask = back_sub.apply(cinza)
     
    # close gaps using closing (morphology)
    fg_mask = cv2.morphologyEx(fg_mask,cv2.MORPH_CLOSE,kernel)
       
    # Remove noise with a median filter
    # fg_mask = cv2.medianBlur(fg_mask,5)
    
    # threshold to detection
    _, fg_mask = cv2.threshold(fg_mask, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
 
    # Find contours of the object
    contours, hierarchy = cv2.findContours(fg_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    areas = [cv2.contourArea(c) for c in contours]
  
    # If there are no countours
    if len(areas) < 1:
        return frame, [320,240], [320,240]
  
    else:
        # largest moving object
        max_index = np.argmax(areas)
       
    # Draw bounding box
    cnt = contours[max_index]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(frame,(reduc*x,reduc*y),(reduc*(x+w),reduc*(y+h)),(0,255,0),3)

    return frame, [reduc*x,reduc*y], [reduc*(x+w),reduc*(y+h)]
