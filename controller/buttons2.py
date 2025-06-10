import RPi.GPIO as GPIO
import time
import threading
import subprocess
import os

GPIO.setmode(GPIO.BOARD)

# Use PUD_UP because Cherry MX connects to GND when pressed
BUTTON1_PIN = 37
BUTTON2_PIN = 36

GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Lock state to prevent bouncing/repeat
button1_locked = False
button2_locked = False

def unlock_button1():
    global button1_locked
    button1_locked = False

def unlock_button2():
    global button2_locked
    button2_locked = False

def button1_callback(channel):
    global button1_locked
    if not button1_locked:
        button1_locked = True
        print("Button 1 pressed")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(BASE_DIR, "scripts/redraw.sh")
        subprocess.run([script_path])
        threading.Timer(5.0, unlock_button1).start()

def button2_callback(channel):
    global button2_locked
    if not button2_locked:
        button2_locked = True
        print("Button 2 pressed")
        # Your button 2 action here
        threading.Timer(5.0, unlock_button2).start()

# Register callbacks
GPIO.add_event_detect(BUTTON1_PIN, GPIO.FALLING, callback=button1_callback, bouncetime=200)
GPIO.add_event_detect(BUTTON2_PIN, GPIO.FALLING, callback=button2_callback, bouncetime=200)

try:
    print("Listening for button presses...")
    while True:
        time.sleep(1)  # keep the main thread alive

except KeyboardInterrupt:
    GPIO.cleanup()