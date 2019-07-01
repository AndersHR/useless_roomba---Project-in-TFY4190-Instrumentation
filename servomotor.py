import RPi.GPIO as GPIO
from numpy import load, savez
import time

#global constants
filename = "angle_of_servo.npz"

def angle_to_dc(angle):
    return ((angle/90)*5 + 6.8)

def dc_to_angle(dc):
    return ((dc - 6.8)/5)*90

def get_angle():
    file = load(filename)
    angle = file["angle"]
    return float(angle)

def set_angle(angle):
    savez(filename,angle=angle)

class ServoMotor:
    def __init__(self,servo_pin):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.pin = servo_pin
        
        GPIO.setup(servo_pin,GPIO.OUT)
        self.p = GPIO.PWM(servo_pin, 50)
        self.angle = get_angle()
        
        self.increment = 2
        self.sleep_time = 0.02
        
        self.p.start(angle_to_dc(self.angle))
        
        self.reset_angle()
        
        print("\nServo motor initialized\nPin =","{:}".format(servo_pin))
    
    def cleanup(self):
        set_angle(self.angle)
        self.p.ChangeDutyCycle(0)
        self.p.stop()
        GPIO.output(self.pin,GPIO.LOW)
        GPIO.cleanup()
        print("servo cleanup complete")
        
    def turn(self,angle):
        if((70 <= int(angle)) or (int(angle) <= -70)):
            return
        elif(int(self.angle) == int(angle)):
            return
        
        if self.angle < angle:
            sgn = -1
        else:
            sgn = 1
            
        try:
            while (int(sgn*angle) < int(sgn*self.angle)):
                #print(self.angle)
                self.angle -= (sgn*self.increment)
                self.p.ChangeDutyCycle(angle_to_dc(self.angle))
                time.sleep(self.sleep_time)
                #print(self.angle)

        except KeyboardInterrupt:
            self.cleanup()
    
    def reset_angle(self):
        self.turn(0)
        self.angle = 0

if __name__ == "__main__":
    servo = ServoMotor(22)
    servo.turn(0)
    servo.cleanup()