#########################################
#	UNLV Senior Design
#	Autonomous Object Finding Robot
#	Ian Yanga - CPE
#	Justin Swinney - CPE
#	Ashim Ghimire
#	Matthew Parker
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

# Setup GPIO ports for output

GPIO.setup("P8_14", GPIO.OUT)
GPIO.setup("P8_15", GPIO.OUT)
GPIO.setup("P8_16", GPIO.OUT)
GPIO.setup("P8_17", GPIO.OUT)

# Enable PWM ports
PWM.start(right, 0)
PWM.start(left, 0)

#########################################

#########################################
# Motor Functions

def claw_in_motion():
	PWM.start(arm, 93, 50, 1)	# arm stabilizes to middle point, 180 degrees
	PWM.start(claw, 88, 50, 1)	# open claw all the way
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


def stop():
	GPIO.output("P8_14", GPIO.LOW)
	GPIO.output("P8_15", GPIO.LOW)
	GPIO.output("P8_16", GPIO.LOW)
	GPIO.output("P8_17", GPIO.LOW)
	return None


def pickup_object():
	PWM.start(arm, 93.75, 50, 1) # arm reaches lowest point to pick up object
	time.sleep(1.5)
	PWM.start(claw, 95, 50, 1) # claw closes to pick up object
	time.sleep(1.5)
	PWM.start(arm, 89, 50, 1) # arm brings object all the way up
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

def release_object():
	PWM.start(arm, 92, 50, 1) # arm reaches highest point
	time.sleep(1.5)
	PWM.start(claw, 88, 50, 1) # claw releases object
	time.sleep(1.5)
	return None


#########################################

# Main

if __name__ == '__main__':

    claw_in_motion()
    forward()
    time.sleep(1)	# move forward for 1 second
    stop()
    pickup_object()
    backward()
    time.sleep(1)	# move backward for 1 second
    stop()
    spin()
    time.sleep(2)	# spin for 2 seconds 
    stop()
    release_object()

