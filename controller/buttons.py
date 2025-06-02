import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 1
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 2

while True:
    if GPIO.input(37) == GPIO.HIGH:
        print("Button 1 pressed")
        # Add your button 1 action here
    if GPIO.input(36) == GPIO.HIGH:
        print("Button 2 pressed")
        # Add your button 2 action here