from gpiozero import LED
from time import sleep

led_pin = 21 
led = LED(led_pin)

def led2off():
    led.off()
    print("blue LED is OFF")

led2off()
