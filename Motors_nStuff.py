#!/usr/bin/python
from gpiozero import DistanceSensor
from gpiozero import LED
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import time
import atexit

# globalize steps and motors
m1_steps_taken = 0
m2_steps_taken = 0


#Request length parameters by user, convert from inches to centimeters for the distance reader
lengthTotal = int(input('Input total required rod length in inches [in]: '))
lengthRodEnd = int(input('Input required distance between rod end and bearing center in inches [in]: '))

#Request angle
FinalAngle = int(input('Input required final bearing angle [deg]: '))

#Request thread orientation:
ThreadType = int(input('Specify rod thread type, Normal Thread (1) or Reverse Thread (2): '))

mh = Adafruit_MotorHAT()

# turn off motors automatically at shutdown
def turnOffMotors():
    	zeroMotor(1)
    	zeroMotor(2)
   	 mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

# step the motor and count to maintain angle
def doM1StepAndCount(direction=Adafruit_MotorHAT.FORWARD, step_type=Adafruit_MotorHAT.DOUBLE):
   	 global m1_steps_taken
   	 global myStepper1
    	increment = 1 if direction==Adafruit_MotorHAT.FORWARD else -1
   	 myStepper1.oneStep(direction, step_type)
   	 m1_steps_taken = (m1_steps_taken + increment) % STEPS_PER_ROTATION

def doM2StepAndCount(direction=Adafruit_MotorHAT.FORWARD, step_type=Adafruit_MotorHAT.DOUBLE):
    	global m2_steps_taken
    	global myStepper2
    	increment = 1 if direction==Adafruit_MotorHAT.FORWARD else -1
   	myStepper2.oneStep(direction, step_type)
   	m2_steps_taken = (m2_steps_taken + increment) % STEPS_PER_ROTATION

# move the motors back to 0 degrees
def zeroMotor(motor_num=0):
    	if(motor_num==1):
        	angleMotor1(0)
    	elif(motor_num==2):
        	angleMotor2(0)

#led = LED(5) # test LED?

#Define both distance sensors
sensor1 = DistanceSensor(echo=12, trigger=13)
sensor2 = DistanceSensor(echo=16, trigger=19)

# HOW TO MOVE A MOTOR: 
# https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-stepper-motors

STEPS_PER_ROTATION = 200

def angleMotor1(target_angle=FinalAngle):
	global m1_steps_taken
	target_steps = int(target_angle * STEPS_PER_ROTATION / 360) % STEPS_PER_ROTATION
	m1_direction = Adafruit_MotorHAT.FORWARD
	while(m1_steps_taken!=target_steps):
		doM1StepAndCount(m1_direction)

def angleMotor2(target_angle=FinalAngle):
	global m2_steps_taken
	target_steps = int(target_angle * STEPS_PER_ROTATION / 360) % STEPS_PER_ROTATION
	m2_direction = Adafruit_MotorHAT.BACKWARD
	while(m2_steps_taken!=target_steps):
		doM1StepAndCount(m2_direction)

#set stepper motor variables
myStepper1 = mh.getStepper(STEPS_PER_ROTATION, 1)
myStepper2 = mh.getStepper(STEPS_PER_ROTATION, 2)

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

# Check which direction to move by ThreadType
direction = Adafruit_MotorHAT.FORWARD if ThreadType == 1 else Adafruit_MotorHAT.BACKWARD

while(distanceRead1 > lengthRodEnd):  
   	 doM1StepAndCount(direction,Adafruit_MotorHAT.DOUBLE)
   	 print('Distance Sensor 1: ', distanceRead1)
   	 distanceRead1 = sensor1.distance * 100 / 2.54

# MOTOR TWO
distanceRead2 = sensor2.distance * 100 / 2.54
while(distanceRead1 + distanceRead2 > lengthTotal):
    	doM2StepAndCount(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    	print('Distance Sensor 2: ', distanceRead2)
    	distanceRead2 = sensor2.distance * 100 / 2.54

#add reverse function if length becomes too short
while(distanceRead1+distanceRead2 < lengthTotal):
   	 doM2StepAndCount(Adafruit_MotorHAT.BACKWARD,Adafruit_MotorHAT.MICROSTEP)

angleMotor1(FinalAngle)
angleMotor2(FinalAngle)

# release holders

# reset motor positions, zeroMotor takes the number of the motor, ie 1 for myStepper1
zeroMotor(1)
zeroMotor(2)
