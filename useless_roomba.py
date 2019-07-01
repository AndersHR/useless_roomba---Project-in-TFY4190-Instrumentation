import RPi.GPIO as GPIO
import random
import time as time

from distance_sensor import DistanceSensor
from servomotor import ServoMotor
from dcmotor import DCMotor

class Roomba:
    def __init__(self, MotorE, MotorA, MotorB, servo_pin, trigger, echo,green,yellow,red,distance_timer):
        
        GPIO.setwarnings(False)
        
        self.distance_timer = distance_timer
        
        self.dcmotor = DCMotor(MotorE, MotorA, MotorB)
        self.servomotor = ServoMotor(servo_pin)
        self.distancesensor = DistanceSensor(trigger,echo)
        
        self.green = green
        self.yellow = yellow
        self.red = red
        
        GPIO.setup(self.green,GPIO.OUT)
        GPIO.setup(self.yellow,GPIO.OUT)
        GPIO.setup(self.red,GPIO.OUT)
    
    def red_ON(self):
        GPIO.output(self.red,GPIO.HIGH)
    def red_OFF(self):
        GPIO.output(self.red,GPIO.LOW)
    def yellow_ON(self):
        GPIO.output(self.yellow,GPIO.HIGH)
    def yellow_OFF(self):
        GPIO.output(self.yellow,GPIO.LOW)
    def green_ON(self):
        GPIO.output(self.green,GPIO.HIGH)
    def green_OFF(self):
        GPIO.output(self.green,GPIO.LOW)
        
    
    def cleanup(self):
        GPIO.setup(self.green,GPIO.LOW)
        GPIO.setup(self.yellow,GPIO.LOW)
        GPIO.setup(self.red,GPIO.LOW)
        
        self.servomotor.cleanup()
        self.dcmotor.cleanup()
        self.distancesensor.cleanup()
        
        GPIO.cleanup()
    
    def reverse_turn(self,direction = 1):

        self.dcmotor.stop()
        self.servomotor.turn(direction*50)
        time.sleep(0.5)
    
        while True:
        
            print("reverse")
        
            self.dcmotor.change_speed(100)
            self.dcmotor.backward()
            time.sleep(0.8)
            self.dcmotor.stop()
        
            dist = self.distancesensor.get_distance()
            if dist > 60:
                break
    
        self.servomotor.turn(0)
        time.sleep(0.5)
        self.dcmotor.change_speed(90)
        self.dcmotor.forward()
        
    
    def random_turn(self):
        LAG = 0.4
        
        if (random.random() < 0.5):
            direction = +1
        else:
            direction = -1
        print("turning")
    
        self.dcmotor.change_speed(90)
    
        while True:
        
            dist = self.distancesensor.get_distance()
 
            if dist > 100:
                time.sleep(LAG)
                print("turn complete")
                self.servomotor.turn(0)
                self.dcmotor.change_speed(80)
                print(self.servomotor.angle)
                break
            elif 80 < dist <= 100:
                self.servomotor.turn(direction*10)
            elif 60 < dist <= 80:
                self.servomotor.turn(direction*30)
            elif 40 < dist <= 60:
                self.servomotor.turn(direction*50)
            elif dist <= 20:
                print("stopped while turning")
                self.dcmotor.stop()
                self.reverse_turn(direction)
                break
        
    
            time.sleep(self.distance_timer)