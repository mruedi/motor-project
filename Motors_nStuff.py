#!/usr/bin/python
from gpiozero import DistanceSensor
from gpiozero import LED
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import time
import atexit

mh = Adafruit_MotorHAT()

# turn off motors automatically at shutdown
def turnOffMotors():
    zeroMotor(mh.getMotor(1))
    zeroMotor(mh.getMotor(2))
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

# keep steps count
global steps_taken = 0

# step the motor and count to maintain angle
def doStepAndCount(motor, direction=Adafruit_MotorHAT.FORWARD, step_type=Adafruit_MotorHAT.DOUBLE):
    global steps_taken
    increment = 1 if direction==Adafruit_MotorHAT.FORWARD else -1
    motor.oneStep(direction, Adafruit_MotorHAT.DOUBLE)
    steps_taken = (steps_taken + increment) % STEPS_PER_ROTATION

# move the motor back to 0 degrees
def zeroMotor(motor):
    global steps_taken
    direction = Adafruit_MotorHAT.FORWARD if steps_taken>100 else Adafruit_MotorHAT.BACKWARD
    while(steps_taken!=0):
        doStepAndCount(motor,direction)

#Request length parameters by user, convert from inches to centimeters for the distance reader
lengthTotal = int(input('Input total required rod length in inches [in]: '))*2.54
lengthRodEnd = int(input('Input required distance between rod end and bearing center in inches [in]: '))*2.54

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

STEPS_PER_ROTATION = 200

#set stepper motor variables
myStepper1 = mh.getStepper(STEPS_PER_ROTATION, 1)
myStepper2 = mh.getStepper(STEPS_PER_ROTATION, 2)
#set speed in RPM of steppers
myStepper1.setSpeed(30)
myStepper2.setSpeed(30)

# MOTOR ONE
distanceRead1 = sensor1.distance * 100
# if its farther than an inch away, move a full inch?
# while(distanceRead1 > lengthRodEnd + 1):
#     myStepper1.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
#     print('Distance Sensor 1: ', distanceRead1)
#     distanceRead1 = sensor1.distance * 100
while(distanceRead1 > lengthRodEnd):
    # when it gets close, slow it down for more precision
    # if(distanceRead1 < lengthRodEnd + 1):
    #     myStepper1.setSpeed(30)
    if ThreadType == 1:
        doStepAndCount(myStepper1,Adafruit_MotorHAT.FORWARD,Adafruit_MotorHAT.DOUBLE)
        print('Distance Sensor 1: ', distanceRead1)
        distanceRead1 = sensor1.distance * 100
    else
        doStepAndCount(myStepper1,Adafruit_MotorHAT.BACKWARD,Adafruit_MotorHAT.DOUBLE)
        print('Distance Sensor 1: ', distanceRead1)
        distanceRead1 = sensor1.distance * 100

# MOTOR TWO
distanceRead2 = sensor2.distance * 100
while(distanceRead1 + distanceRead2 > lengthTotal):
    doStepAndCount(myStepper2, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    print('Distance Sensor 2: ', distanceRead2)
    distanceRead2 = sensor2.distance * 100

# release holders

# reset motor positions
zeroMotor(myStepper1)
zeroMotor(myStepper2)

#add reverse function if length becomes too short
while(distanceRead1+distanceRead2 < lengthTotal):
    doStepAndCount(myStepper2,Adafruit_MotorHAT.BACKWARD,Adafruit_MotorHAT.MICROSTEP)