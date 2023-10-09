from security import sendAlarm, addToTheLog, capture_photo

def catch_burglar():
    # capture the burglar face
    capture_photo()

    # Add date to log file
    addToTheLog("Intruder detected!\n")

    # operate buzzer
    sendAlarm()

catch_burglar()