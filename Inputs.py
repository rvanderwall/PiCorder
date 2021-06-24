import sys
import termios
import atexit
from select import select

import pygame
from Logger import Logger


BUTTON_A = 0
BUTTON_B = 1
BUTTON_C = 2
BUTTON_QUIT = 3


def get_mode_select():
    # bit 0 => TFT
    # bit 1 => Demo 
    return 1


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
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        return sys.stdin.read(1)

    def kbhit(self):
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []


class KBInput:
    def __init__(self, logger: Logger):
        self.kb = KBHit()
        self._log = logger.info
        self.current_button = None

    def get_button_press(self):
        if self.kb.kbhit():
            c = self.kb.getch()
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
        self.kb.set_normal_term()


class ButtonPress:
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
