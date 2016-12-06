import subprocess
from random import random
import random
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from camera_pi import Camera
import RPi.GPIO as GPIO
import time
import os
import time
import atexit

GPIO.setmode(GPIO.BCM)

TRIG = [24, 22]
ECHO = [23, 27]


def do(cmd):
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def setup():
    for i in range(len(TRIG)):
        GPIO.setup(TRIG[i], GPIO.OUT)
        GPIO.setup(ECHO[i], GPIO.IN)
        GPIO.output(TRIG[i], False)

        print "Waiting For Sensor To Settle"


def distance(i):
#    print "Distance Measurement In Progress"

    GPIO.output(TRIG[i], True)

    time.sleep(0.00001)

    GPIO.output(TRIG[i], False)

    pulse_end = 0;
    pulse_start = 0;

    while GPIO.input(ECHO[i])==0:
        pulse_start = time.time()

    while GPIO.input(ECHO[i])==1:
        pulse_end = time.time()

    if (pulse_end == 0 or pulse_start==0):
        return 1000

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

 #   print "Distance:",distance,"cm"

    return distance

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	#mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	#mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
        GPIO.cleanup()

atexit.register(turnOffMotors)

################################# DC motor test!
mFL = mh.getMotor(1)
#mBL = mh.getMotor(2)
#mBR = mh.getMotor(3)
mFR = mh.getMotor(3)


def wakeup(m):
    # set the speed to start, from 0 (off) to 255 (max speed)
    m.setSpeed(150)
    m.run(Adafruit_MotorHAT.FORWARD);
    # turn on motor
    m.run(Adafruit_MotorHAT.RELEASE);


wakeup(mFL)
#wakeup(mBL)
wakeup(mFR)
#wakeup(mBL)
setup()


def gof():
    #mBR.run(Adafruit_MotorHAT.BACKWARD)
    #mBL.run(Adafruit_MotorHAT.BACKWARD)
    mFL.run(Adafruit_MotorHAT.FORWARD)
    mFR.run(Adafruit_MotorHAT.FORWARD)
    #mBR.setSpeed(200)
    #mBL.setSpeed(200)
    mFR.setSpeed(200)
    mFL.setSpeed(200)


def setSpeed(speed):
    #mBR.setSpeed(speed)
    #mBL.setSpeed(speed)
    mFR.setSpeed(speed)
    mFL.setSpeed(speed)


def backward(speed, dur):
	print "Backward! "
	mFR.run(Adafruit_MotorHAT.BACKWARD)
	mFL.run(Adafruit_MotorHAT.BACKWARD)
	mFR.setSpeed(speed)
	mFL.setSpeed(speed)
	time.sleep(dur)

	mFL.run(Adafruit_MotorHAT.RELEASE)
	mFR.run(Adafruit_MotorHAT.RELEASE)
	return ''


def stop():
    mFL.run(Adafruit_MotorHAT.RELEASE)
    mFR.run(Adafruit_MotorHAT.RELEASE)
    #mBL.run(Adafruit_MotorHAT.RELEASE)
    #mBR.run(Adafruit_MotorHAT.RELEASE)


def left(speed, dur):
    print "Left "
    mFR.run(Adafruit_MotorHAT.BACKWARD)
    mFR.setSpeed(speed)

    time.sleep(dur)
    mFR.run(Adafruit_MotorHAT.RELEASE)
    return ''


def right(speed, dur):
    print "Right "
    mFL.run(Adafruit_MotorHAT.BACKWARD)
    mFL.setSpeed(speed)

    time.sleep(dur)
    mFL.run(Adafruit_MotorHAT.RELEASE)
    return ''


def getAttention():
    with open('../python-mindave-mobile/ATTENTION', 'r') as f:
        read_data = f.read()
        print("Read Speed: " + read_data)

    spd = 0
    if read_data == '':
        spd = 0
    else:
        spd = int(read_data)

    if (spd < 50):
        newSpd = 0
    else:
        newSpd = (spd-50)*4

    return newSpd
