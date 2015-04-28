# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 19:42:43 2015

@author:
"""
LOG = True

# <InstanceID> + log + <number>
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

DIRECTORY = r'/root'

def get_picture():
    os.system('python /root/takepic.py')
    pic = cv2.imread('/root/temp.png')
    temp = pic[:,:,0]
    pic[:,:,0] = pic[:,:,2]
    pic[:,:,2] = temp
    return pic

def get_picture_self(capture):
    while True:
        ret,frame = camera.read()
        if ret == False:
            print('Retrying')
            time.sleep(2)
        else:
            break
    pic = np.array(frame)
   # temp = pic[:,:,2]
   # pic[:,:,2] = pic[:,:,0]
   # pic[:,:,0] = temp    
    return pic    

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def where_dat_ball(rgbimg):
    mypic = copy.deepcopy(rgbimg)
    ratioimg = np.float32(rgbimg[:,:,0])/(np.float32(rgbimg[:,:,1])+np.float32(rgbimg[:,:,2]))
    mymask = ratioimg>1.4
    opened = nd.morphology.binary_opening(mymask,iterations=5)    
    [labels,num_labels] = nd.label(opened)

    largest_mask_size = 0 
    best_com = (1,1)
    best_size = 0
    best_avg_ratio = 0
    for x in range(1,num_labels+1):
        region_mask = labels==x
        com = nd.measurements.center_of_mass(region_mask)
        object_size = np.sum(region_mask)
        if object_size > largest_mask_size:
            best_com = com
            best_size = object_size
            best_avg_ratio = np.mean(ratioimg[region_mask])
    return best_com, best_size, best_avg_ratio, mymask

def rotate_to_find_ball():
    noop = 0

if LOG:
    file_list = os.listdir(DIRECTORY)
    instance = 0     
    
    while True: 
        filename = 'Instance_' + str(instance) + '_Pic_' + '0001.png'
        if filename in file_list:
            instance += 1
            continue
        else:
            break

    picnum = 0

phase = 'seek'
counter = 0

camera = cv2.VideoCapture(0)
camera.set(3,352)
camera.set(4,288)
#capture = cv.CaptureFromCAM(
camera.set(12, 0.5)

while True:
    counter += 1
    log = 'Second is ' + str(counter) + '\n'
    log += 'Start Phase: ' + str(phase) + '\n'
    
    # Get an Image
    #imgtemp = r'C:\Users\Chad\Desktop\pingpong\image0006.jpg'
    #img = PIL.Image.open(imgtemp)
    #orig = np.asarray(img)    
    #log += 'Loaded Image.\n'
    t0 = time.time()
    if True:
        orig = get_picture_self(camera) 
    else:
        orig = get_picture()    
    print('Image Capture: ' + str(time.time()-t0) + ' seconds.')    

    # Compute where the ball is
    t0 = time.time()
    center_of_mass, size, ratio, notorig = where_dat_ball(orig)
    print('Image Processing: ' + str(time.time()-t0) + ' seconds.')
    log += 'center_of_mass = %.2f , %.2f'%(center_of_mass[0],center_of_mass[1]) + '\n'
    log += 'size = ' + str(size) + '\n'
    log += 'ratio = ' + str(ratio) + '\n'
    # Do the appropriate action based on what phase we are in
    if phase == 'seek' and size == 0:
        t0 = time.time()
#        robot.spin_left()
        print('Did not Detect Ball. Spin: ' + str(time.time()-t0) + ' seconds.')
        log += 'WHERE YOU AT BALL!??! TURNING LEFT\n'
    else:
        robot.stop()	    
        log += 'GOT YOU MUTHA FUCKA! STOP!\n'
        print('I see it. Not Moving')

    # If log mode save log
    t0 = time.time()
    if LOG:
        log += 'End Phase: ' + str(phase)  
        #if counter % 2 != 0:
        #    continue
        picnum += 1
        zerostring = '000'
        if picnum > 9:
            zerostring = '00'
        if picnum > 99:
            zerostring = '0'
        if picnum > 999:
            zerostring = ''
        filename = 'Instance_' + str(instance) + '_Pic_' + zerostring + str(picnum) + '.png'
        fullname = os.path.join(DIRECTORY, filename)
        fig = plt.figure(1)
        
        frame = plt.subplot2grid((1,2),(0,0))
        frame.imshow(orig)
        plt.text(center_of_mass[1], center_of_mass[0], '+', fontsize=60, color='green',verticalalignment='center', horizontalalignment='center') 
        
        
        frame = plt.subplot2grid((1,2),(0,1))
        frame.text(0.1,0.9,log, transform=frame.transAxes, va='top', ha='left', fontsize=8)
        frame.axes.get_xaxis().set_visible(False)            
        frame.axes.get_yaxis().set_visible(False)   
        frame.patch.set_visible(False)
        frame.axis('off') 
       
        print 'Saving Log...'
        plt.savefig(fullname)

        print('Log Save Time: ' + str(time.time()-t0) + ' seconds.')

# For All Time, Every Second
    # Compute where the ball is 
    # If Phase = 1?2?3?
        # Do appropriate Phase STuff
    # If log file is true, save log file
