from gpiozero import AngularServo
from time import sleep

# Set up the servo on GPIO pin 18
servo = AngularServo(18)

def open_door():
    servo.angle = 20
    sleep(0.1)

def close_door():
    servo.angle = -48
    sleep(0.1)

def stop_servo():
    servo.angle = None
    sleep(2)

open_door()
stop_servo()
close_door()