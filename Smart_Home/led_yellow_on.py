from gpiozero import LED
from time import sleep

led_pin = 20 
led = LED(led_pin)

def led1on():
    while True:
        led.on()
    
led1on()