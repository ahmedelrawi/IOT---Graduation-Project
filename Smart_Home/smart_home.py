from gpiozero import DistanceSensor,LED
from time import sleep
import Adafruit_DHT
from signal import pause

# setting up ultrasonic sensor on GPIO pins 22 and 27
sensor = DistanceSensor(echo=27, trigger=22)

#setting up DHT11 sensor on GPIO pin 4
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 16

#setting up LEDs on differnt GPIO pins
green_led = LED(26)

white_led = LED(23)



# function to get current measured distance in cm
def get_distance():
    # printting distance to console
    distance = round(sensor.distance * 100,2)
    # print('Distance: \n', distance)
    # returning distance in cm
    return distance



humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)


# function to read DHT11 sensor humidity and temperature
def get_humidity_temperature():
    reading humidity and temperature from DHT11 sensor on GPIO pin 20
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    printing humidity and temperature to console
    print('Humidity: ', humidity)
    print('Temperature: \n', temperature)
    returning humidity and temperature
    return humidity, temperature

while True:
    # calling function to get distance
    if get_distance() > 10 or temperature > 27:
        green_led.on()
        green_led.blink(1)
    else:
        green_led.off()

    # calling function to get humidity and temperature
    get_humidity_temperature()
    

    if get_distance() > 40 :
        white_led.off()
    else:
        white_led.on()

    sleep(1)
