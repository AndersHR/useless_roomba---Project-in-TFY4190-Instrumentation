import RPi.GPIO as GPIO
import time

class DCMotor:
    def __init__(self,MotorE,MotorA,MotorB,speed=50):
        GPIO.setmode(GPIO.BCM)
        
        self.MotorE = MotorE
        self.MotorA = MotorA
        self.MotorB = MotorB
        
        GPIO.setup(MotorE,GPIO.OUT)
        GPIO.setup(MotorA,GPIO.OUT)
        GPIO.setup(MotorB,GPIO.OUT)
        
        self.p = GPIO.PWM(MotorE,100)
        self.p.start(speed)
        
        print("\nDC Motor initialized\nMotor Enable =","{:}".format(MotorE),
                                      "\nMotor A =","{:}".format(MotorA),
                                      "\nMotor B =","{:}".format(MotorB))
    
    def change_speed(self,speed):
        self.p.ChangeDutyCycle(speed)
    
    def forward(self):
        
        GPIO.output(self.MotorA,GPIO.HIGH)
        GPIO.output(self.MotorB,GPIO.LOW)
        GPIO.output(self.MotorE,GPIO.HIGH)
    
    def backward(self):
        
        GPIO.output(self.MotorA,GPIO.LOW)
        GPIO.output(self.MotorB,GPIO.HIGH)
        GPIO.output(self.MotorE,GPIO.HIGH)
    
    def stop(self):
        GPIO.output(self.MotorE,GPIO.LOW)
        GPIO.output(self.MotorA,GPIO.LOW)
        GPIO.output(self.MotorB,GPIO.LOW)
    
    def cleanup(self):
        self.p.stop()
        GPIO.cleanup()
        print("dc cleanup complete")

if __name__ == "__main__":
    time.sleep(1)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20,GPIO.OUT)
    GPIO.output(20,GPIO.HIGH)
    
    time.sleep(1)
    
    dcmotor = DCMotor(5,13,19,70)
    dcmotor.forward()
    time.sleep(5)
    GPIO.output(20,GPIO.LOW)
    dcmotor.stop()

    
    dcmotor.cleanup()
