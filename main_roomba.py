import RPi.GPIO as GPIO
import time
import random

from useless_roomba import Roomba

distance_timer = 0.1

if __name__ == "__main__":
    
    MotorE = 5
    MotorA = 13
    MotorB = 19
    servo_pin = 22
    trigger = 17
    echo = 4
    green = 20
    yellow = 16
    red = 12
    
    roomba = Roomba(MotorE, MotorA, MotorB, servo_pin, trigger, echo,green,yellow,red,distance_timer)
    roomba.dcmotor.change_speed(60)
    
    try:
        time.sleep(10)
        roomba.red_ON()
        time.sleep(1)
        roomba.red_OFF()
        roomba.yellow_ON()
        time.sleep(1)
        roomba.yellow_OFF()
        roomba.green_ON()
        time.sleep(1)
        roomba.green_OFF()
        print("GO")
        
        roomba.dcmotor.forward()
        for i in range(200):        #for-loop instead of while-loop for testing purposes
            dist = roomba.distancesensor.get_distance()
            #print(roomba.distancesensor.get_distance())
        
            if 100 < dist < 140:
                roomba.dcmotor.change_speed(90)
            elif dist < 100:
                roomba.random_turn()
            elif dist > 140:
                roomba.dcmotor.change_speed(100)
        
            time.sleep(roomba.distance_timer)
    except KeyboardInterrupt:
        roomba.dcmotor.stop()
        roomba.cleanup()
    
    roomba.dcmotor.stop()
    
    roomba.cleanup()
    