# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 19:42:43 2015

@author:
"""
     
LOG = False

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

#global camera

DIRECTORY = r'/root'

def get_picture():
    os.system('python /root/takepic.py')
    pic = cv2.imread('/root/temp.png')
    return pic

def get_picture_self(capture):
    while True:
        #camera = camera_setup()
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
    #camera.release()
    #camera = camera_setup()
    return pic    

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def where_dat_ball(rgbimg):
    mypic = copy.deepcopy(rgbimg)
    ratioimg = np.float32(rgbimg[:,:,0])/(np.float32(rgbimg[:,:,1])+np.float32(rgbimg[:,:,2]))
    mymask = ratioimg>1.0
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

def get_angle_from_com(com):
    return np.rad2deg(np.arctan((com[1]-189.32)/(400-com[0])))

def estimate_turn_time(angle):
    angle = np.float32(np.abs(angle))
   # turn_time = 2.73e-6*angle*angle + 7.68e-3*angle + 3.76e-2
    turn_time = -8.82e-6*angle*angle + 4.792e-3*angle + 2.7538e-2   
    if turn_time>.25:
        turn_time = .25
    return turn_time

def flush_buffer(camera):
    flush_init_time = time.time()
    while(time.time()- flush_init_time) < 2.0:
        camera.grab   
    
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

def camera_setup():
    cam = cv2.VideoCapture(0)
    cam.set(3,352)
    cam.set(4,288)
    #capture = cv.CaptureFromCAM(
    cam.set(12, 0.5)
    return cam
    

#camera = camera_setup()
while True:
    #if camera.isOpened() == False:
    #    camera = camera_setup()
    LOG = False
    counter += 1
    log = 'Second is ' + str(counter) + '\n'
    log += 'Start Phase: ' + str(phase) + '\n'
    
    # Get an Image
    #imgtemp = r'C:\Users\Chad\Desktop\pingpong\image0006.jpg'
    #img = PIL.Image.open(imgtemp)
    #orig = np.asarray(img)    
    #log += 'Loaded Image.\n'
    t0 = time.time()
    #if phase == 'seek':
    if False:
        orig = get_picture_self(camera) 
    else:
        orig = get_picture()    
    print('Image Capture: ' + str(time.time()-t0) + ' seconds.')    

    # Compute where the ball is
    t0 = time.time()
    center_of_mass, size, ratio, notorig = where_dat_ball(orig)
    print('CenterOfMass = '+ str(center_of_mass) + '\n')
    print('Size = ' + str(size) + '\n')
    print('Image Processing: ' + str(time.time()-t0) + ' seconds.')
    log += 'center_of_mass = %.2f , %.2f'%(center_of_mass[0],center_of_mass[1]) + '\n'
    log += 'size = ' + str(size) + '\n'
    log += 'ratio = ' + str(ratio) + '\n'
    # Do the appropriate action based on what phase we are in
    if phase == 'seek' and size == 0:
        t0 = time.time()
        #robot.spin_right(45)
        print('Did not Detect Ball. Spin: ' + str(time.time()-t0) + ' seconds.')
        log += 'Did not find ball, turning right.\n'
    
    if phase == 'seek' and size != 0:
        phase = 'turn'
        robot.stop()
        #camera.release()
        #del camera
        #time.sleep(3)	    
        log += 'Found Object, Centering.\n'
        print('Found Object, Moving to Turn Phase')

    if phase == 'turn':
        LOG = False
        if size == 0:
            phase == 'seek'
            #robot.spin_left(3)
            #robot.spin_right(55)
           # camera = camera_setup()
            s = 'Ball Lost, Seeking'
            log += s
            print(s)
            continue
    
        angle = get_angle_from_com(center_of_mass)
        if angle > -10 and angle < 10:
           # phase = 'move'
            robot.arm_init()
            s = 'Angle Good. Going to Move Phase'           
            print (s)
            log += s
            
            #if center_of_mass[0] == 1:
             #  robot.timed_backward(.07,60)
            if center_of_mass[0]> 270:
                  robot.pickup()
                  robot.spinfortime(.6,25,True)
                  robot.timed_forward(.3, 45)
                  robot.dropoff()
                  robot.arm_init()
            else:
                    robot.timed_forward(.06,55)
                    if center_of_mass[0] == 1:
                       robot.timed_backward(.07,60)
                    if center_of_mass[0]> 230 and center_of_mass[0] < 270:
                       robot.timed_forward(.02,27)
                       
            
        else:
            turn_left = angle<0
            turn_time = np.float32(estimate_turn_time(angle))
            turn_time = turn_time
            print('Turning: ')
            print('  Turn Angle:' + str(angle))
            print('  Turn Time: ' + str(turn_time))
            robot.spinfortime(turn_time,100,turn_left)
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
