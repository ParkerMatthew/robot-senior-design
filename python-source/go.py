"""
This program will:
1. Find toys
2. place toys on red box

save a copy for github!
C:\Users\schoo\Documents\GitHub\robot-senior-design\python-source\
C:\Users\Matthew\Documents\GitHub\robot-senior-design\python-source\
"""
#
# Constants - change these if you need to
#
LOG = False
CLAW_ANGLE = 5.6 # use this constant for the angle needed to be centered
CLAW_DISTANCE = 250 # use this constant for the center_of_mass[0] value needed to be close enough
BOX_DISTANCE = 258
BOX_ANGLE = 10
MID_X = 190 # middle of claw X value
POWER = 1.00 # percent of battery. increase when low battery. use 0.75 when super charged.
##
##

# <InstanceID> + log + <number>
import os
import matplotlib.pyplot as plt
import time
import numpy as np
import copy
import scipy.ndimage as nd
import cv2.cv as cv
import robot
import cv2

DIRECTORY = r'/root'

def get_picture():
    #takes a single picture that should be up to date
    robot.stop()
    time.sleep(0.35) # maybe the camera is taking blurry pictures
    os.system('python /root/takepic.py')
    time.sleep(0.60)
    pic = cv2.imread('/root/temp.png')
    time.sleep(0.35)
    return pic
    
def show_picture():
    #display image, requires user to press a button to continue
    imgFile = cv2.imread('temp.png')
    cv2.imshow('angle less than 10', imgFile)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return None

def get_picture_self(capture):
    #read from the camera contuously, will have 2 second lag
    while True:
        ret,frame = capture.read()
        if ret == False:
            print('retrying camera read')
            time.sleep(2)
        else:
            break
    pic = np.array(frame)
    return pic

def find_color(rgbimg, color):
    mypic = copy.deepcopy(rgbimg)
    #[:,:,0] blue.  [:,:,1] green.  [:,:,2] red.
    if(color == "red"):
        ratioimg = np.float32(rgbimg[:,:,2])/(np.float32(rgbimg[:,:,1])+np.float32(rgbimg[:,:,0]))
    elif (color == "green"):
        ratioimg = np.float32(rgbimg[:,:,1])/(np.float32(rgbimg[:,:,2])+np.float32(rgbimg[:,:,0]))
    elif (color == "blue" or True):
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
            largest_mask_size = object_size
            best_com = com
            best_size = object_size
            best_avg_ratio = np.mean(ratioimg[region_mask])
    return best_com, best_size, best_avg_ratio, mymask
    
def rotate_to_find_ball():
    noop = 0

def get_angle_from_com(com):
    return np.rad2deg(np.arctan((com[1] - MID_X)/(400-com[0])))

def estimate_turn_time(angle):
    angle = np.float32(np.abs(angle))
    #turn_time = 2.73e-6*angle*angle + 7.68e-3*angle + 3.76e-2
    turn_time = -8.82e-6*angle*angle + 4.792e-3*angle + 2.7538e-2   
    if turn_time>.25:
        turn_time = .25
    return turn_time
 
def log_init():
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
    
def camera_setup():
    cam = cv2.VideoCapture(0)
    cam.set(3,352)
    cam.set(4,288)
    cam.set(11,0.14) #contrast, default 0.125
    cam.set(12, 0.14) #saturation, default is 0.125. 0.19 seems to work well.
    return cam
    
def check_if_holding():
    #ToDo: actually check using camera
    return True

def go():
    #This is the main function
    
    
    ball_was_found = False #Used to check if the last movement caused the ball to be lost
    box_was_found = False
    ball_is_held = False
    camera_is_reading = False # used to know if camera is already reading
    phase = 'turn' #starting phase should be seek when done
    last_phase = phase
    seek_direction = 0 # 0 for right, 1 for left. Will alternate
    counter = 0
    
    if LOG:
        log_init()
    
    #Experimental variables:
    old_x = -999 # not used when doing angle instead of X coordinate
    old_y = -999
    old_angle = -999
    good_angle = False
    
    
    #use power adjustment for turning to center
    #use time adjustment for movement forward
    power_high = 1.00 
    power_low = 0.40
    time_high = 1.00
    time_low = 0.40
    
    power_percent = 0.75 # start high (original code used 100% duty PWM for turning)
    time_percent = time_low # start small
    
    
    robot.arm_highest()
    robot.claw_open()
    while True:
        
        counter += 1
        log = 'Second is ' + str(counter) + '\n'
        log += 'Start Phase: ' + str(phase) + '\n'
        
        if phase == 'seek':
            if(camera_is_reading == False):
                camera_is_reading = True
                camera = camera_setup()
            orig = get_picture_self(camera) # read from camera for real time with 2 second lag
        else:
            if (camera_is_reading == True):
                camera_is_reading = False
                camera.release()
            orig = get_picture()  # get 1 picture for up to date images
        
        if(ball_is_held):
            color = "red"
        else:
            color = "blue"
        center_of_mass, size, ratio, notorig = find_color(orig, color)
        angle = get_angle_from_com(center_of_mass)
        
        if(old_x == -999 or old_y == -999 or old_angle == -999):
            #this should only happen once
            old_x = center_of_mass[1]
            old_y = center_of_mass[0]
            old_angle = angle
        
        #d meaning delta = change in the value
        dx = old_x - center_of_mass[1]
        dy = old_y - center_of_mass[0]
        da = old_angle - angle
        old_y = center_of_mass[0]
        old_x = center_of_mass[1]
        
        #calculate changing amount of time/power
        if ((ball_is_held == False) and ( abs(angle) > CLAW_ANGLE )) or ((ball_is_held == True) and ( abs(angle) > BOX_ANGLE )):
            #we're trying to fix angle
            if (good_angle == True):
                # the angle is now bad, so reset the percents
                time_percent = time_low 
                power_percent = power_high
                good_angle = False
            if (abs(dx) > abs(center_of_mass[1]-MID_X)):
                power_percent -= 0.20
            else:
                if (abs(dx) < abs(center_of_mass[1]-MID_X)*0.9):
                    power_percent += 0.10
        else:
            #we're trying to fix distance
            if(good_angle == False): 
                # the angle is now good, so reset the percents
                time_percent = time_low
                power_percent = power_high
                good_angle = True
            if ((ball_is_held == False) and (abs(dy) < abs(center_of_mass[0] - CLAW_DISTANCE)*0.8)) or ((ball_is_held == True) and (abs(dy) < abs(center_of_mass[0] - BOX_DISTANCE)*0.8)):
                time_percent += 0.30
            else:
                if ball_is_held == False:
                    if abs(dy) > abs(center_of_mass[0] - CLAW_DISTANCE):
                        time_percent -= 0.20
                if ball_is_held == True:
                    if abs(dy) > abs(center_of_mass[0] - BOX_DISTANCE):
                        time_percent -= 0.20
                        
        #percents should always be between 0 and 1, and within the HIGH and LOW constants set above
        power_percent = min(max(power_percent, power_low), power_high)
        time_percent = min(max(time_percent, time_low), time_high)
        
        print "dx = ", dx, ", dy = ", dy, ", da = ", da
        print "pp = ", power_percent, ", tp = ", time_percent
        print('CenterOfMass = '+ str(center_of_mass) + '\n')
        print "angle = ",angle
        print('Size = ' + str(size) + '\n')
        log += 'center_of_mass = %.2f , %.2f'%(center_of_mass[0],center_of_mass[1]) + '\n'
        log += 'size = ' + str(size) + '\n'
        
        
        if((box_was_found == True or ball_was_found == True) and size == 0):
            #we lost the ball after moving.
            ball_was_found = False
            box_was_found = False
            if(last_phase == 'seek'):
                #Assume went too far right (or left)
                print "Size is 0 after ball was found. Assuming that we turned too far"
                turn_time = 1.0 # Assume angle is somewhere to the left/right
                seek_direction = not seek_direction
                robot.spinfortime(turn_time,75*POWER, seek_direction)
                
            elif (last_phase == 'turn'):
                #Assume we moved too far forward.
                time_percent = time_low
                print "Size is 0 after ball was found, assuming that we went too far forward"
                #show_picture() #!! DEBUG ONLY
                robot.timed_backward(.14*time_percent,65*POWER)
                orig = get_picture()
                center_of_mass, size, ratio, notorig = find_color(orig, color)   
        last_phase = phase
        
        # Do the appropriate action based on what phase we are in
        if phase == 'seek':
            if size == 0:
                print('Did not Detect Ball. Spinning' )
                print "seek_direction = ", seek_direction
                log += 'Did not find ball, spinning.\n'
                robot.spin(30*POWER, seek_direction)
            else:
                phase = 'turn'
                robot.stop()
                #camera.release()
                #del camera
                #time.sleep(3)	    
                log += 'Found Object, Centering.\n'
                print('Found Object, Moving to Turn Phase')
        
        if phase == 'turn':
            if size == 0:
                ball_was_found = False
                box_was_found = False
                phase = 'seek'
                s = 'Ball Lost, Seeking'
                log += s
                print(s)
            else:
                ball_was_found = True
                box_was_found = True
            if abs(angle) < CLAW_ANGLE or ((ball_is_held == True) and abs(angle) < BOX_ANGLE):
                robot.arm_highest()
                s = 'Angle Good. Going to Move Phase'           
                print (s)
                log += s
                
                if center_of_mass[0] > CLAW_DISTANCE or ((ball_is_held == True) and (center_of_mass[0] > BOX_DISTANCE)):
                    if(ball_is_held == False):
                        robot.pickup()
                        ball_is_held = check_if_holding()
                        ball_was_found = False
                        robot.arm_highest()
                    else:
                        robot.release()
                        ball_is_held = False
                    #Done:
                        cv2.destroyAllWindows()
                        print "\n\nJob Complete. Sleeping for 10 seconds. Press Ctrl+Z to quit.\n"
                        time.sleep(10)
                   # exit()
                else:
                    if(ball_is_held):
                        robot.timed_forward(time_percent*0.14,power_percent*100*POWER)
                    else:
                        robot.timed_forward(time_percent*0.10,power_percent*100*POWER)
            else:
                turn_left = angle<0
                turn_time = np.float32(estimate_turn_time(angle))
                print('Turning: ')
                print('  Turn Angle:' + str(angle))
                print('  Turn Time: ' + str(turn_time))
                robot.spinfortime(turn_time,75*power_percent*POWER,turn_left)
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
        # End LOG
    # end While
    robot.stop_all()
    cv2.destroyAllWindows()
    return None
    
    
if __name__ == '__main__':
    go()
