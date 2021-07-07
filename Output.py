from Logger import Logger
try:
    import RPi.GPIO as GPIO
    USE_HW_LEDS = True
except:
    USE_HW_LEDS = False

PWM0_PIN = 12  # GPIO 12 / Pin 32
LED1_PIN = 13  # GPIO 13 / Pin 33
LED2_PIN = 19  # GPIO 19 / Pin 35
LED3_PIN = 26  # GPIO 26 / Pin 37


class LEDBank:
    def __init__(self, logger: Logger):
        GPIO.setmode(GPIO.BCM)  # Use BCM GPIO Numbering Scheme

        GPIO.setup(LED1_PIN, GPIO.OUT)
        GPIO.setup(LED2_PIN, GPIO.OUT)
        GPIO.setup(LED3_PIN, GPIO.OUT)

        self._red = 0
        self._yellow = 0
        self._blue = 0

    def turn_on_led(self, led_num):
        GPIO.output(led_num, 1)

    def turn_off_led(self, led_num):
        GPIO.output(led_num, 0)


class MockLEDBank:
    def __init__(self, logger: Logger):
        self._log = logger.info

    def turn_on_led(self, led_num):
        self._log(f"Turn on led {led_num}")

    def turn_off_led(self, led_num):
        self._log(f"Turn off led {led_num}")


class LEDS:
    def __init__(self, logger: Logger):
        self._red_led = LED1_PIN
        self._yellow_led = LED2_PIN
        self._blue_led = LED3_PIN

        if USE_HW_LEDS:
            self._leds = LEDBank(logger)
        else:
            self._leds = MockLEDBank(logger)

    def turn_on_red_led(self):
        self._leds.turn_on_led(self._red_led)

    def turn_off_red_led(self):
        self._leds.turn_off_led(self._red_led)

    def turn_on_yellow_led(self):
        self._leds.turn_on_led(self._yellow_led)

    def turn_off_yellow_led(self):
        self._leds.turn_off_led(self._yellow_led)

    def turn_on_blue_led(self):
        self._leds.turn_on_led(self._blue_led)

    def turn_off_blue_led(self):
        self._leds.turn_off_led(self._blue_led)
