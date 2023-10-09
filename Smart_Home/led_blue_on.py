from gpiozero import LED
from time import sleep

led_pin = 21 
led = LED(led_pin)

def led2on():
    while True:
        led.on()
    
led2on()