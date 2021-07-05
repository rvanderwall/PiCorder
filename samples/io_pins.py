from time import sleep
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)  # Use BCM GPIO Numbering Scheme


# GPIO21, pin 40
INPUT_PIN = 21
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set it as input pin


OUTPUT_PIN = 20
GPIO.setup(OUTPUT_PIN, GPIO.OUT)  # Set it as output pin


while True:
    in_val = GPIO.input(INPUT_PIN)
    if in_val == 0:
        GPIO.output(OUTPUT_PIN, 1)
    else:
        GPIO.output(OUTPUT_PIN, 0)
    print(f"Pin {INPUT_PIN} = {in_val}")
    sleep(1)


GPIO.cleanup()
