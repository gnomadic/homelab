import RPi.GPIO as GPIO
import time
import threading
import subprocess

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button 1
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button 2

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
        if GPIO.input(37) == GPIO.HIGH and not button1_locked:
            button1_locked = True
            print("Button 1 pressed")
            # Add your Button 1 action here
            subprocess.run(["scripts/refresh.sh"])
            threading.Timer(5.0, unlock_button1).start()

        if GPIO.input(36) == GPIO.HIGH and not button2_locked:
            button2_locked = True
            print("Button 2 pressed")
            # Add your Button 2 action here
            threading.Timer(5.0, unlock_button2).start()

        time.sleep(0.05)  # Slight delay to reduce CPU usage

except KeyboardInterrupt:
    GPIO.cleanup()