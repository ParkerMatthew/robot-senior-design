#tests

#Don't forget to save to github:

import cv
import os
import matplotlib.pyplot as plt
import time
#import PIL
import numpy as np
import copy
import scipy.ndimage as nd
import cv2.cv as cv
import robot
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,352)
cap.set(4,288)
cap.set(5,1) # 1 frame per second, doesn't seem to change anything
        
counter = 0
while(True):
    counter += 1
    if (counter > 100):
        break
    else:
        print 'frame ',counter,' out of 100'
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    #img= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = frame
    #cv2.imshow('frame',frame)
    cv2.imshow('image', img)
    cv2.waitKey(1) # image will not display without waitkey()
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
exit()


# Single image capture
while True:
    capture = cv.CaptureFromCAM(0)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 288)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 352)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FORMAT, cv.IPL_DEPTH_32F)

    img = cv.QueryFrame(capture)
    #cv2.startWindowThread()
    cv.imshow("image",img) # causes error
    this_is_supposed_to_fix_error = cv.WaitKey(10)
    time.sleep(2)
    
    
