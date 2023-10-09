import datetime
from time import sleep
from picamera import PiCamera
from gpiozero import DistanceSensor, LED, Buzzer
from client import post_image

red_led = LED(26)
camera_sensor   = PiCamera()
# distance_sensor = DistanceSensor(echo=27, trigger=22)

def sendAlarm():
    red_led.on()
    bz = Buzzer(6)
    bz.on()
    sleep(2)
    bz.off()
    red_led.off()


def returnFormatedTime():
     return  datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]


def addToTheLog(message):
    with open("log_file.log", 'a') as log_file:
            log_file.write(f"{returnFormatedTime()} --> {message}")


def capture_photo():
    try:
        # saving in images directory
        image_path = "/home/abcd/Desktop/Project_106/Images"

        # generating name as a date 
        image_name = f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]}.jpg"

        # Construct the full file path
        full_image_path = f"{image_path}/{image_name}"

        # Capture an image
        camera_sensor.capture(full_image_path)
        
        # upload to firebase, make sure that server.py is running
        post_image(full_image_path, image_name)

        print(f"Image saved at: {full_image_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def logIn():
    for i in range(3):
        password_input = input("Enter the password: ")
        if password_input == "password":
            print("Login successful.")
            addToTheLog("Login successful\n")
            return True
        else:
            print(f"Invalid login attempt ({i+1}/3)\n")
            addToTheLog("Invalid login attempt.\n")
            if i == 2:
                addToTheLog("Intruder detected!\n")
                capture_photo()
                sendAlarm()
                return False


