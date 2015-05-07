#tests

#Don't forget to save to github:
# file->save a copy as... -> name the file "C:\Users\schoo\Documents\GitHub\robot-senior-design\python-source\test.py"

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

test_count = 0
DIRECTORY = r'/root'

while (test_count < 1):
    test_count += 1
    cap = cv2.VideoCapture(0)
    cap.set(3,352)
    cap.set(4,288)
    cap.set(5,1) # 1 frame per second, doesn't seem to change anything
            
    counter = 0
    while(True):
        counter += 1
        if (counter > 20):
            break
        else:
            print 'frame ',counter,' out of 20'
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
    #exit()


    # Single image capture
    os.system('python /root/takepic.py')