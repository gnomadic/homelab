import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # Use BCM for GPIO26
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        state = GPIO.input(26)
        print("GPIO26 (pin 37) state:", "LOW (pressed)" if state == GPIO.LOW else "HIGH (released)")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()