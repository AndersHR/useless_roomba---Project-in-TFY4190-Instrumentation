#Libraries
import RPi.GPIO as GPIO
import time


class DistanceSensor:
    def __init__(self,trigger,echo):
        GPIO.setmode(GPIO.BCM)
        
        self.trigger = trigger
        self.echo = echo
        
        GPIO.setup(trigger,GPIO.OUT)
        GPIO.setup(echo,GPIO.IN)
        
        print("\nDistance sensor initialized\nTrigger =","{:}".format(trigger),
                                              "\nEcho =","{:}".format(echo))
    
    def get_distance(self):
        GPIO.output(self.trigger,GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger,GPIO.LOW)
        
        StartTime = time.time()
        StopTime = time.time()
 

        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
 
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
 
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
         
        print ("Measured Distance = %.1f cm" % distance)
        return distance
    
    def cleanup(self):
        GPIO.cleanup()
        print("distance sensor cleanup complete")
            
