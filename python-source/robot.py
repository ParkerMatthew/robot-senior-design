#########################################
#    UNLV Senior Design
#    Autonomous Object Finding Robot
#    Ian Yanga - CPE
#    Justin Swinney - CPE
#    Ashim Ghimire - CPE
#    Matthew Parker - CPE
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
    PWM.start(claw, 89, 50, 1)    # open claw all the way
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

def timed_forward(t,duty):
    PWM.set_duty_cycle(right, duty)
    PWM.set_duty_cycle(left, duty)
    PWM.set_frequency(right, 75)
    PWM.set_frequency(left, 75)

    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_15", GPIO.HIGH)
    GPIO.output("P8_16", GPIO.LOW)
    GPIO.output("P8_17", GPIO.HIGH)
    
    time.sleep(t)
    
    GPIO.output("P8_15", GPIO.LOW)
    GPIO.output("P8_17", GPIO.LOW)
    return None

def timed_backward(t,duty):
    PWM.set_duty_cycle(right, duty)
    PWM.set_duty_cycle(left, duty)
    PWM.set_frequency(right, 75)
    PWM.set_frequency(left, 75)

    GPIO.output("P8_14", GPIO.HIGH)
    GPIO.output("P8_15", GPIO.LOW)
    GPIO.output("P8_16", GPIO.HIGH)
    GPIO.output("P8_17", GPIO.LOW)
    
    time.sleep(t)
    
    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_16", GPIO.LOW)
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

def arm_highest():
    PWM.start(arm, 88, 50, 1) # as high as it can go
    return None
    
def arm_down():
    PWM.start(arm, 93.75, 50, 1)
    return None

def arm_lowest():
    PWM.start(arm, 94.1, 50, 1)
    return None

def claw_open():
    PWM.start(claw, 88.7, 50, 1) # above 88.7, the claw is slightly closed. 88.7 and below are all the same
    return None
    
def claw_close():
    PWM.start(claw, 96, 50, 1) # 96 is a little tighter than 95
    return None
    
def claw_tightest():
    PWM.start(claw, 97.5, 50, 1) # 96 is a little tighter than 95
    return None

# Use this function to try to prevent the claw from getting too hot. 
# it is possible to hold an object while relaxed, but it can slip out while moving around.
def claw_relax():
    # PWM.stop(claw) # After calling this function, the next claw_close or claw_open will take 45 seconds to start.
    PWM.start(claw, 0, 50, 1)  # a PWM of 0 will allow it to cool down without making it lag.
    return None
    
def pickup():
    # pickup
    arm_up()
    claw_open()
    time.sleep(1)
    arm_down()
    time.sleep(2)
    arm_lowest() # some objects are short
    time.sleep(0.25)
    claw_close()
    time.sleep(1.5)
    claw_tightest() # sometimes the claw won't close all the way
    time.sleep(0.5)
    arm_up()
    #claw_relax() # this might cause the object to slip, but it will cool down the claw motor.
    time.sleep(2)
    return None
    
def release():
    # release
    arm_down()
    time.sleep(0.5)
    claw_open()
    time.sleep(1.0)
    arm_up()
    claw_relax()
    return None
    
def demo():
    pickup()
    release()
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
    
def spin(duty, left):
    if(left):
        spin_left(duty)
    else:
        spin_right(duty)
    return None

def spinfortime(t, duty, left):
        if left:
            spin_left(duty)
        else:
            spin_right(duty)
        time.sleep(t)
        stop()

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


