from gpiozero import LED
from time import sleep

led_pin = 20 
led = LED(led_pin)

def led1off():
    led.off()
    print("yellow LED is OFF")

led1off()
