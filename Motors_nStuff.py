#!/usr/bin/python
from gpiozero import DistanceSensor
from gpiozero import LED
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import time
import atexit

mh = Adafruit_MotorHAT()

# turn off motors automatically at shutdown
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

#Request length parameters by user
lengthTotal = int(input('Input total required rod length in inches [in]: '))
lengthRodEnd = int(input('Input required distance between rod end and bearing center in inches [in]: '))

#Request angle
FinalAngle = int(input('Input required final bearing angle [deg]: '))

#Request thread orientation:
ThreadType = int(input('Specify rod thread type, Normal Thread (1) or Reverse Thread (2): '))

#led = LED(5) # test LED?

#Define both distance sensors
sensor1 = DistanceSensor(echo=12, trigger=13)
sensor2 = DistanceSensor(echo=16, trigger=19)

# HOW TO MOVE A MOTOR: 
# https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-stepper-motors

#set stepper motor variables
myStepper1 = mh.getStepper(200, 1)
myStepper2 = mh.getStepper(200, 2)
#set speed in RPM of steppers
myStepper1.setSpeed(30)
myStepper2.setSpeed(30)

# MOTOR ONE
distanceRead1 = sensor1.distance * 100 / 2.54
# if its farther than an inch away, move a full inch?
# while(distanceRead1 > lengthRodEnd + 1):
#     myStepper1.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
#     print('Distance Sensor 1: ', distanceRead1)
#     distanceRead1 = sensor1.distance * 100 / 2.54
while(distanceRead1 > lengthRodEnd):
    # when it gets close, slow it down for more precision
    # if(distanceRead1 < lengthRodEnd + 1):
    #     myStepper1.setSpeed(30)
    if ThreadType == 1:
        myStepper1.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
        print('Distance Sensor 1: ', distanceRead1)
        distanceRead1 = sensor1.distance * 100 / 2.54
    else
        myStepper1.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE
        print('Distance Sensor 1: ', distanceRead1)
        distanceRead1 = sensor1.distance * 100 / 2.54

# MOTOR TWO
distanceRead2 = sensor2.distance * 100 / 2.54
while(distanceRead1 + distanceRead2 > lengthTotal):
    myStepper2.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    print('Distance Sensor 2: ', distanceRead2)
    distanceRead2 = sensor2.distance * 100 / 2.54

# release holders
# reset motor positions

#add reverse function if length becomes too short

