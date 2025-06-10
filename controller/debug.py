import RPi.GPIO as GPIO
import time
import threading
import subprocess
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 1
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 2

# Button state locks
button1_locked = False
button2_locked = False

def unlock_button1():
    global button1_locked
    button1_locked = False

def unlock_button2():
    global button2_locked
    button2_locked = False

try:
    while True:
        if not button1_locked:
            button1_locked = True
            # print("Button 1 pressed")
            input1 = GPIO.input(37)
            print("Button 2 pressed: " + str(input1))
            # Add your Button 1 action here
            # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            # script_path = os.path.join(BASE_DIR, "scripts/redraw.sh")
            # subprocess.run([script_path])
            threading.Timer(1.0, unlock_button1).start()

        if not button2_locked:
            # button2_locked = True
            input2 = GPIO.input(36)
            print("Button 2 pressed: " + str(input2))
            # Add your Button 2 action here
            threading.Timer(1.0, unlock_button2).start()

        time.sleep(.8)  # Slight delay to reduce CPU usage

except KeyboardInterrupt:
    GPIO.cleanup()