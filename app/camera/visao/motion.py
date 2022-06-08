import cv2
import numpy as np


# Create the background subtractor object
# Feel free to modify the history as you see fit.
back_sub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=25, detectShadows=True)

# Create kernel for morphological operation. You can tweak
# the dimensions of the kernel.
# e.g. instead of 20, 20, you can try 30, 30
kernel = np.ones((50,50),np.uint8)

def motion(frame):

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (linhas, colunas) = cinza.shape
    cinza = cv2.resize( cinza, (colunas//2, linhas//2) )
    frame = cv2.resize( frame, (colunas//2, linhas//2) )
    
    # Convert to foreground mask
    # fg_mask = back_sub.apply(frame)
    fg_mask = back_sub.apply(cinza)
     
    # Close gaps using closing
    fg_mask = cv2.morphologyEx(fg_mask,cv2.MORPH_CLOSE,kernel)
       
    # Remove salt and pepper noise with a median filter
    # fg_mask = cv2.medianBlur(fg_mask,5)
    
    # If a pixel is less than ##, it is considered black (background). 
    # Otherwise, it is white (foreground). 255 is upper limit.
    # Modify the number after fg_mask as you see fit.
    _, fg_mask = cv2.threshold(fg_mask, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
 
    # Find the contours of the object inside the binary image
    contours, hierarchy = cv2.findContours(fg_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    areas = [cv2.contourArea(c) for c in contours]
  
    # If there are no countours
    if len(areas) < 1:
        # frame = cv2.resize( frame, (linhas, colunas))
        return frame
  
    else:
         
      # Find the largest moving object in the image
      max_index = np.argmax(areas)
       
    # Draw the bounding box
    cnt = contours[max_index]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

    # frame = cv2.resize( frame, (linhas, colunas))

    return frame
