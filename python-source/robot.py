#########################################
#    UNLV Senior Design
#    Autonomous Object Finding Robot
#    Ian Yanga - CPE
#    Justin Swinney - CPE
#    Ashim Ghimire
#    Matthew Parker
#########################################

#########################################
# Import Python Libraries

import time
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import cv2

#########################################

#########################################
# Define variables

right = "P8_13"
left = "P8_19"
claw = "P9_42"
arm = "P9_16"

# Enable PWM ports for DC motors
PWM.start(right, 0)
PWM.start(left, 0)
# Setup GPIO ports for output

GPIO.setup("P8_14", GPIO.OUT)
GPIO.setup("P8_15", GPIO.OUT)
GPIO.setup("P8_16", GPIO.OUT)
GPIO.setup("P8_17", GPIO.OUT)

#########################################

#########################################
# Motor Functions

def claw_in_motion():
    PWM.start(arm, 93, 50, 1)    # arm stabilizes to middle point, 180 degrees
    PWM.start(claw, 88, 50, 1)    # open claw all the way
    return None


def forward():
    PWM.set_duty_cycle(right, 50)
    PWM.set_duty_cycle(left, 50)
    PWM.set_frequency(right, 75)
    PWM.set_frequency(left, 75)

    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_15", GPIO.HIGH)
    GPIO.output("P8_16", GPIO.LOW)
    GPIO.output("P8_17", GPIO.HIGH)
    return None

#Stop the DC motors
def stop():
    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_15", GPIO.LOW)
    GPIO.output("P8_16", GPIO.LOW)
    GPIO.output("P8_17", GPIO.LOW)
    return None

#Emergency Stop - call before exiting python / main
def stop_all():
    stop()
    PWM.stop(claw)
    PWM.stop(arm)
    PWM.cleanup()
    return None

def arm_up():
    PWM.start(arm, 92, 50, 1) # not as high as it can go
    return None

def arm_down():
    PWM.start(arm, 93.75, 50, 1)
    return None

def claw_open():
    PWM.start(claw, 88, 50, 1)
    return None

# Use this function to try to prevent the claw from getting too hot. 
# Don't expect the claw to work for awhile after calling.
def claw_relax():
    PWM.stop(claw)
    return None

def claw_close():
    PWM.start(claw, 97, 50, 1) # 97 is a little tighter than 95
    return None

def demo():
    # pickup
    arm_up()
    claw_open()
    time.sleep(1)
    arm_down()
    time.sleep(1)
    claw_close()
    time.sleep(2)
    arm_up()
    time.sleep(2)
    
    # release
    arm_down()
    time.sleep(0.5)
    claw_open()
    time.sleep(0.75)
    arm_up()
    
    return None
    
def pickup_object():
    PWM.start(arm, 93.75, 50, 1) # arm reaches lowest point to pick up object
    time.sleep(1.5)
    PWM.start(claw, 95, 50, 1) # claw closes to pick up object
    time.sleep(1.5)
    PWM.start(arm, 92, 50, 1) # arm brings object up
    time.sleep(1.5)
    return None
    
def release_object():
    PWM.start(arm, 92, 50, 1) # arm reaches highest point
    time.sleep(1.5)
    PWM.start(claw, 88, 50, 1) # claw releases object
    time.sleep(1.5)
    return None

def spin_right(duty):
    PWM.set_duty_cycle(right, duty)
    PWM.set_duty_cycle(left, duty)
    PWM.set_frequency(right, 200)
    PWM.set_frequency(left, 200)

    GPIO.output("P8_14", GPIO.HIGH)
    GPIO.output("P8_15", GPIO.LOW)
    GPIO.output("P8_16", GPIO.LOW)
    GPIO.output("P8_17", GPIO.HIGH)
    return None

def spin_left(duty):
    PWM.set_duty_cycle(right, duty)
    PWM.set_duty_cycle(left, duty)
    PWM.set_frequency(right, 200)
    PWM.set_frequency(left, 200)

    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_15", GPIO.HIGH)
    GPIO.output("P8_16", GPIO.HIGH)
    GPIO.output("P8_17", GPIO.LOW)
    return None

def spinfortime(t, duty, left):
        if left:
            spin_left(duty)
        else:
            spin_right(duty)
        time.sleep(t)
        stop()

def two():
    PWM.set_duty_cycle(right, 50)
    PWM.set_duty_cycle(left, 50)
    PWM.set_frequency(right, 200)
    PWM.set_frequency(left, 200)

    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_15", GPIO.HIGH)
    GPIO.output("P8_16", GPIO.LOW)
    GPIO.output("P8_17", GPIO.HIGH)
    
    time.sleep(.3)
    GPIO.output("P8_15", GPIO.LOW)
    GPIO.output("P8_14", GPIO.HIGH)
    return None

def backward():
    PWM.set_duty_cycle(right, 50)
    PWM.set_duty_cycle(left, 50)
    PWM.set_frequency(right, 75)
    PWM.set_frequency(left, 75)

    GPIO.output("P8_14", GPIO.HIGH)
    GPIO.output("P8_15", GPIO.LOW)
    GPIO.output("P8_16", GPIO.HIGH)
    GPIO.output("P8_17", GPIO.LOW)
    return None

def turn_right_degrees(angle):
        dtime = -.000258*angle*angle + .01273*angle+2.74e-2 + .01753
        spin_right(100)
        time.sleep(dtime)
        stop()




#########################################

# Main

if __name__ == '__main__':

    claw_in_motion()
    forward()
    time.sleep(1)    # move forward for 1 second
    stop()
    pickup_object()
    backward()
    time.sleep(1)    # move backward for 1 second
    stop()
    spin()
    time.sleep(2)    # spin for 2 seconds 
    stop()
    release_object()

