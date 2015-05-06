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
import gogo

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
    
    
    
    #Save a picture with COM displayed
    orig = cv2.imread('/root/temp.png')
    center_of_mass, size, ratio, notorig = gogo.where_dat_ball(orig)
    
    
    log = "log\n"
    log += 'center_of_mass = %.2f , %.2f'%(center_of_mass[0],center_of_mass[1]) + '\n'
    log += 'size = ' + str(size) + '\n'    
    #picnum += 1
    #zerostring = '000'
    #if picnum > 9:
    #    zerostring = '00'
    #if picnum > 99:
    #    zerostring = '0'
    #if picnum > 999:
    #    zerostring = ''
    filename = 'temp2.png'
    fullname = os.path.join(DIRECTORY, filename)
    fig = plt.figure(1)
    frame = plt.subplot2grid((1,2),(0,0))
    #frame.imshow(orig)
    plt.text(center_of_mass[1], center_of_mass[0], '+', fontsize=60, color='green',verticalalignment='center', horizontalalignment='center') 
    frame = plt.subplot2grid((1,2),(0,1))
    frame.text(0.1,0.9, log, transform=frame.transAxes, va='top', ha='left', fontsize=8)
    frame.axes.get_xaxis().set_visible(False)            
    frame.axes.get_yaxis().set_visible(False)   
    frame.patch.set_visible(False)
    frame.axis('off') 
    #print 'Saving Log...'
    plt.savefig(fullname)
    #print('Log Save Time: ' + str(time.time()-t0) + ' seconds.')
        
        