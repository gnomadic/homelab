import RPi.GPIO as GPIO
import time
import sys

# --- Configuration ---
# IMPORTANT: Set the correct GPIO pin for your Inky display's BUSY signal.
# For Inky pHAT, it's typically 24
# For Inky wHAT, it's typically 17
BUSY_PIN = 17 # <--- CHANGE THIS TO YOUR INKY'S BUSY PIN

# --- Script ---
def monitor_busy_pin(pin):
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF) # Inky typically handles pull-ups externally

    print(f"Monitoring GPIO {pin} (BUSY signal) for 10 seconds. Press Ctrl+C to stop.")
    print("Pin state: HIGH (idle/ready) | LOW (busy)")

    try:
        start_time = time.time()
        while time.time() - start_time < 10: # Monitor for 10 seconds
            pin_state = GPIO.input(pin)
            if pin_state == GPIO.LOW:
                print(f"[{time.time() - start_time:.2f}s] BUSY pin is LOW (display is busy or stuck)")
            else:
                print(f"[{time.time() - start_time:.2f}s] BUSY pin is HIGH (display is idle/ready)")
            time.sleep(0.5) # Check every 0.5 seconds

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        GPIO.cleanup() # Clean up GPIO settings on exit

if __name__ == "__main__":
    if BUSY_PIN is None:
        print("ERROR: Please set the BUSY_PIN variable in the script to your Inky's busy pin.")
        sys.exit(1)
    monitor_busy_pin(BUSY_PIN)