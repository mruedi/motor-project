#!/usr/bin/python
from gpiozero import DistanceSensor
from gpiozero import LED
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import time
import atexit

#Request length parameters by user
lengthTotal = int(input('Input total required rod length in inches [in]: '))
lengthRodEnd = int(input('Input required distance between rod end and bearing center in inches [in]: '))
led = LED(5)
#Define both distance sensors
sensor1 = DistanceSensor(echo=12, trigger=23)
sensor2 = DistanceSensor(echo= , trigger= )
while True:
    distanceRead1 = sensor1.distance * 100 / 2.54   #Set distance to a variable and convert to inches from mm
    distanceRead2 = sensor2.distance * 100 / 2.54
    print('Distance Sensor 1: ', distanceRead1)
    print('Distance Sensor 2: ', distanceRead2)

    if(distanceRead1 > lengthRodEnd):
        led.on() #Motor 1 should be running
    else:
        led.off() #Should shut down motor 1 - lengthRodEnd is achieved on one end
    if(distanceRead1 + distanceRead2 > lengthTotal):
        led.on() #This is where motor 2 needs to be activated
    else:
        led.off() #Should shut down motor 2 -  lengthTotal is achieved



#turn off motors automatically at shutdown
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)


atexit.register(turnOffMotors)

#set stepper motor variable
myStepper = mh.getStepper(200, 1)
#set speed in RPM of stepper
myStepper.setSpeed(30)



#add reverse function if length becomes too short

