import sys
import termios
import atexit
from select import select

import pygame
from Logger import Logger

try:
    import RPi.GPIO as GPIO
    USE_HW_BUTTONS = True
except:
    USE_HW_BUTTONS = False


BUTTON1_PIN = 13    # GPIO 13 / Pin 33
BUTTON2_PIN = 19    # GPIO 19 / Pin 35
BUTTON3_PIN = 26    # GPIO 26 / Pin 37

BUTTON_A = 0
BUTTON_B = 1
BUTTON_C = 2
BUTTON_QUIT = 3


def get_mode_select():
    # bit 0 => TFT
    # bit 1 => Demo 
    return 1


class ButtonHit:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # Use BCM GPIO Numbering Scheme

        GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.__button = None

    def set_normal(self):
        GPIO.cleanup()

    def getch(self):
        return self.__button

    def kbhit(self):
        if GPIO.input(BUTTON1_PIN) == 0:
            self.__button = 'a'
            return True

        if GPIO.input(BUTTON2_PIN) == 0:
            self.__button = 'b'
            return True

        if GPIO.input(BUTTON3_PIN) == 0:
            self.__button = 'c'
            return True

        self.__button = None
        return False


class KBHit:
    def __init__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal)

    def set_normal(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        return sys.stdin.read(1)

    def kbhit(self):
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []


class ButtonInput:
    def __init__(self, logger: Logger):
        if USE_HW_BUTTONS:
            self.btnReader = ButtonHit()
        else:
            self.btnReader = KBHit()
        self._log = logger.info
        self.current_button = None

    def get_button_press(self):
        if self.btnReader.kbhit():
            c = self.btnReader.getch()
            if ord(c) == 120 or ord(c) == 27:  # 'x' or ESC
                self._log("You pressed the Done button")
                self.current_button = BUTTON_QUIT
            if ord(c) == ord('a'):
                self._log("You pressed the A button")
                self.current_button = BUTTON_A
            if ord(c) == ord('b'):
                self._log("You pressed the B button")
                self.current_button = BUTTON_B
            if ord(c) == ord('c'):
                self._log("You pressed the C button")
                self.current_button = BUTTON_C
        else:
            self.current_button = None

        return self.current_button

    def close(self):
        self.btnReader.set_normal()


class KeyboardInput:
    def __init__(self, logger: Logger):
        self._log = logger.info
        self.current_button = None

    def get_button_press(self, event):
        # Make sure focus is on the Display window NOT the console!!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._log("You pressed the A button")
                self.current_button = BUTTON_A
            if event.key == pygame.K_b:
                self._log("You pressed the B button")
                self.current_button = BUTTON_B
            if event.key == pygame.K_c:
                self._log("You pressed the C button")
                self.current_button = BUTTON_C
            if event.key == pygame.K_x:
                self._log("You pressed the x button")
                self.current_button = BUTTON_QUIT
        else:
            self.current_button = None

        return self.current_button

    def close(self):
        pass
